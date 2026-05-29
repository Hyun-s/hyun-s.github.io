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
from notifier import DiscordNotifier
from calendar_manager import CalendarManager
from report_generator import ReportGenerator
from typing import List, Dict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("JobCrawlerMain")

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CrawlerState:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.processed_ids = self._load_state()

    def _load_state(self) -> set:
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return set(json.load(f))
        return set()

    def is_processed(self, job_id: str) -> bool:
        return job_id in self.processed_ids

    def mark_as_processed(self, job_id: str):
        self.processed_ids.add(job_id)
        self._save_state()

    def _save_state(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(list(self.processed_ids), f, ensure_ascii=False, indent=2)

def git_commit_and_push(file_path: str):
    """Automatically commit and push changes to the repository"""
    try:
        # Check if there are changes
        status = subprocess.run(["git", "status", "--porcelain", file_path], capture_output=True, text=True, cwd=PROJECT_ROOT)
        if not status.stdout.strip():
            logger.info("Git: No changes to commit")
            return

        subprocess.run(["git", "add", file_path], check=True, cwd=PROJECT_ROOT)
        # Also add reports if any
        subprocess.run(["git", "add", "content/job-report/*.md"], cwd=PROJECT_ROOT)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        subprocess.run(["git", "commit", "-m", f"chore: update job data {date_str}"], check=True, cwd=PROJECT_ROOT)
        subprocess.run(["git", "push", "origin", "main"], check=True, cwd=PROJECT_ROOT)
        logger.info("Git: Successfully pushed changes")
    except Exception as e:
        logger.error(f"Git operation failed: {e}")

def main():
    logger.info("Starting job crawler...")
    load_dotenv()
    
    # Load categories
    categories_path = os.path.join(PROJECT_ROOT, "data", "job-categories.toml")
    with open(categories_path, 'r', encoding='utf-8') as f:
        categories = toml.load(f).get('categories', [])

    # Initialize components
    scraper = CatchScraper()
    llm = LLMProcessor()
    
    discord_webhook = os.getenv("DISCORD_WEBHOOK_URL")
    notifier = DiscordNotifier(discord_webhook) if discord_webhook else DiscordNotifier("")
    
    calendar_id = os.getenv("CALENDAR_ID")
    credentials_json = os.getenv("GCP_CREDENTIALS")
    calendar = CalendarManager(credentials_json, calendar_id) if (calendar_id and credentials_json) else None
    
    state = CrawlerState(os.path.join(PROJECT_ROOT, "data", "processed_ids.json"))
    report_gen = ReportGenerator(os.path.join(PROJECT_ROOT, "content", "job-report"))
    
    # Load existing data
    output_path = os.path.join(PROJECT_ROOT, "data", "jobs.json")
    existing_jobs = []
    if os.path.exists(output_path):
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                existing_jobs = json.load(f)
        except Exception as e:
            logger.error(f"Error loading existing jobs: {e}")
    
    # Map existing jobs by ID for easy update/merging
    jobs_map = {job['id']: job for job in existing_jobs}

    # Step 1: Crawl
    logger.info("Starting Catch.co.kr calendar crawl...")
    new_raw_jobs = scraper.crawl_all_jobs()
    logger.info(f"Total potential jobs found: {len(new_raw_jobs)}")
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    suitable_jobs = []
    new_jobs_count = 0
    
    # Step 2: Process and Classify
    overrides_path = os.path.join(PROJECT_ROOT, "data", "job-overrides.json")
    overrides = {}
    if os.path.exists(overrides_path):
        with open(overrides_path, 'r', encoding='utf-8') as f:
            overrides = json.load(f)

    for job in new_raw_jobs:
        # Only process jobs matching today's date in the calendar
        if job.start_date != today_str and job.end_date != today_str:
            continue

        unique_id = f"{job.source}_{job.id}"
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
                'classified_at': datetime.now().isoformat() + 'Z',
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
                    'summary_data': summary_data,
                    'classified_at': datetime.now().isoformat() + 'Z',
                    'manual_override': False
                }
        
        if job_result:
            # Update or Add to map
            jobs_map[unique_id] = job_result
            
            # Check if really new for notifications/reports
            if not state.is_processed(unique_id):
                s_data = job_result.get('summary_data', {})
                is_manual = job_result.get('manual_override', False)
                is_ai_suitable = s_data.get('is_suitable', False)
                domain = s_data.get('domain', '').lower()
                
                # Only process if it's manual override OR (classified as AI AND deep analysis confirmed suitability AND not None-AI)
                if is_manual or (job_result.get('category') != 'others' and is_ai_suitable and domain not in ['none-ai', 'others']):
                    s_data['deadline'] = job.end_date
                    s_data['domain'] = job_result.get('category')
                    s_data['source'] = job.source

                    notifier.send_job_notification(job.title, job.company, s_data, job.link)
                    if calendar:
                        calendar.add_job_event(job.title, job.company, s_data, job.link)
                    
                    suitable_jobs.append(job_result)
                    state.mark_as_processed(unique_id)
                    new_jobs_count += 1
                elif job_result.get('category') == 'others' or not is_ai_suitable:
                    # Mark as processed even if not suitable, so we don't analyze it again
                    state.mark_as_processed(unique_id)

    # Save all jobs back
    processed_list = list(jobs_map.values())
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(processed_list, f, ensure_ascii=False, indent=2)
    
    # Step 4: Generate Report
    if suitable_jobs:
        report_path = report_gen.generate_daily_report(suitable_jobs)
        logger.info(f"Daily report generated at: {report_path}")

    # Step 5: Git Distribution
    git_commit_and_push(output_path)

    logger.info(f"Job crawling completed. {new_jobs_count} new suitable jobs processed.")

if __name__ == "__main__":
    main()
