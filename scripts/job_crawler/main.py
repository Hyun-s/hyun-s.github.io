import os
import logging
import time
import json
import subprocess
import toml
from datetime import datetime
from dotenv import load_dotenv
from wanted_scraper import WantedScraper
from inthiswork_scraper import InThisWorkScraper
from catch_scraper import CatchScraper
from llm_processor import LLMProcessor
from calendar_manager import CalendarManager, StateManager
from notifier import DiscordNotifier
from report_generator import ReportGenerator

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JobCrawlerMain")

def load_categories():
    """Load category configuration from TOML"""
    path = 'data/job-categories.toml'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = toml.load(f)
            return config.get('categories', [])
    return []

def load_overrides():
    """Load manual overrides if they exist"""
    path = 'data/job-overrides.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def git_commit_and_push(file_path: str):
    """Commit and push changes to maintain the Hugo distribution method"""
    try:
        logger.info(f"Git: Committing and pushing {file_path}")
        subprocess.run(["git", "add", file_path], check=True)
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain", file_path], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", f"chore: update job data {datetime.now().strftime('%Y-%m-%d')}"], check=True)
            subprocess.run(["git", "push"], check=True)
            logger.info("Git: Successfully pushed changes")
        else:
            logger.info("Git: No changes to commit")
    except Exception as e:
        logger.warning(f"Git: Failed to commit and push: {e}. This may be expected in some environments.")

def main():
    # Load Environment Variables from .env file if it exists
    loaded = load_dotenv()
    if loaded:
        logger.info("Successfully loaded .env file")
    else:
        logger.warning(".env file not found or could not be loaded, using existing environment variables")
    
    gemini_api_key = os.getenv("GEMINI_API_KEY", "local")
    gcp_credentials = os.getenv("GCP_CREDENTIALS")
    calendar_id = os.getenv("CALENDAR_ID")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    # Initialize components
    llm = LLMProcessor(gemini_api_key)
    notifier = DiscordNotifier(discord_webhook_url)
    state = StateManager("processed_jobs.json")
    report_gen = ReportGenerator("content/job-report")
    
    # Optional components
    calendar = None
    if gcp_credentials and calendar_id:
        calendar = CalendarManager(gcp_credentials, calendar_id)

    # Load configurations
    categories = load_categories()
    overrides = load_overrides()

    # Step 1: Crawl jobs
    catch_scraper = CatchScraper()
    logger.info("Starting Catch.co.kr calendar crawl...")
    all_jobs = catch_scraper.crawl_all_jobs()
    
    logger.info(f"Total potential jobs found: {len(all_jobs)}")

    processed_data = []
    new_jobs_count = 0
    suitable_jobs = []

    for job in all_jobs:
        unique_id = f"{job.source}_{job.id}"
        
        # 2. Classification & Processing
        job_result = None
        
        # Check for manual override first
        if unique_id in overrides:
            logger.info(f"Using manual override for {unique_id}")
            override_data = overrides[unique_id]
            job_result = {
                'id': unique_id,
                'source': job.source,
                'company': job.company,
                'position': job.title,
                'description': job.description,
                'start_date': job.start_date,
                'end_date': job.end_date,
                'application_url': job.link,
                'category': override_data.get('category'),
                'subcategories': override_data.get('subcategories', []),
                'skills': override_data.get('skills', []),
                'confidence': 1.0,
                'classified_at': datetime.utcnow().isoformat() + 'Z',
                'manual_override': True
            }
        else:
            # Use LLM for classification
            classification = llm.classify_job({
                'company': job.company,
                'title': job.title,
                'description': job.description
            }, categories)
            
            if classification:
                category = classification.get('primary_category')
                
                # If it's a relevant AI category, get a deeper summary
                summary_data = {}
                if category and category != 'others':
                    logger.info(f"Deep analyzing suitable job: {job.company} - {job.title}")
                    summary_data = llm.summarize_job(job.title, job.company, job.description) or {}
                
                job_result = {
                    'id': unique_id,
                    'source': job.source,
                    'company': job.company,
                    'position': job.title,
                    'description': job.description,
                    'start_date': job.start_date,
                    'end_date': job.end_date,
                    'application_url': job.link,
                    'category': category,
                    'subcategories': classification.get('subcategories', []),
                    'skills': classification.get('skills', []),
                    'confidence': classification.get('confidence', 0),
                    'summary_data': summary_data, # Store deep summary
                    'classified_at': datetime.utcnow().isoformat() + 'Z',
                    'manual_override': False
                }
        
        if job_result:
            processed_data.append(job_result)
            
            # Check if new for notifications/reports
            if not state.is_processed(unique_id):
                # Filter/Logic for notifications: notify if AI category or manual override
                if (job_result.get('category') and job_result.get('category') != 'others') or job_result.get('manual_override'):
                    
                    s_data = job_result.get('summary_data', {})
                    # Ensure some basic fields for notifier/calendar
                    s_data['deadline'] = job.end_date
                    s_data['domain'] = job_result.get('category')
                    s_data['source'] = job.source

                    # Notify Discord
                    notifier.send_job_notification(
                        job_title=job.title,
                        company=job.company,
                        summary_data=s_data,
                        link=job.link
                    )
                    
                    # Add to Google Calendar
                    if calendar:
                        calendar.add_job_event(
                            job_title=job.title,
                            company=job.company,
                            summary_data=s_data,
                            link=job.link
                        )
                    
                    # Collect for daily report
                    suitable_jobs.append({
                        'title': job.title,
                        'company': job.company,
                        'link': job.link,
                        'source': job.source,
                        'summary_data': s_data
                    })
                    
                    state.mark_as_processed(unique_id)
                    new_jobs_count += 1

    # Step 3: Save to Hugo data directory
    output_path = 'data/jobs.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Processed {len(processed_data)} jobs -> {output_path}")

    # Step 4: Generate Daily Report
    if new_jobs_count > 0:
        report_path = report_gen.generate_daily_report(suitable_jobs)
        logger.info(f"Daily report generated at: {report_path}")

    # Step 5: Git Distribution
    git_commit_and_push(output_path)

    logger.info(f"Job crawling completed. {new_jobs_count} new suitable jobs processed.")

if __name__ == "__main__":
    main()
