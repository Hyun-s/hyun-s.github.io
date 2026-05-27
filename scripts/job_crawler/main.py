import os
import logging
import time
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
    
    # Validation
    missing_vars = []
    if not gcp_credentials: missing_vars.append("GCP_CREDENTIALS")
    if not calendar_id: missing_vars.append("CALENDAR_ID")
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please ensure these are set in your .env file or environment.")
        return

    # Initialize scrapers
    scrapers = [
        # WantedScraper(),
        InThisWorkScraper(),
        # CatchScraper()
    ]
    
    llm = LLMProcessor(gemini_api_key)
    calendar = CalendarManager(gcp_credentials, calendar_id)
    notifier = DiscordNotifier(discord_webhook_url)
    state = StateManager("processed_jobs.json")
    report_gen = ReportGenerator("content/job-report")

    keywords = ["AI Engineer", 
                "AI Research Scientist", "AI Research Engineer", "AI Research", "AI Researcher",
                "Machine Learning Scientist", "Deep Learning Scientist", 
                "Machine Learning Engineer", "Deep Learning Engineer", 
                "Machine Learning Research Scientist", "Deep Learning Research Scientist", 
                "Machine Learning Researcher", "Deep Learning Researcher", 
                "LLM Engineer", "Computer Vision Engineer"
                ]
    logger.info(f"Starting job crawl for keywords: {keywords}")

    # 1. Search for jobs from all sources
    all_jobs = []
    for scraper in scrapers:
        source_name = scraper.__class__.__name__.replace("Scraper", "")
        logger.info(f"Searching for jobs from source: {source_name}")
        source_jobs = scraper.search_jobs(keywords, limit=20)
        all_jobs.extend(source_jobs)
        logger.info(f"Found {len(source_jobs)} potential jobs from {source_name}.")

    logger.info(f"Total potential jobs found: {len(all_jobs)}")

    new_jobs_count = 0
    suitable_jobs = []
    skipped_count = 0

    for job in all_jobs:
        # Check if already processed
        # Combine source and ID to create a unique identifier if needed, 
        # but here we'll use the ID as provided by the scraper.
        unique_id = f"{job.source}_{job.id}"
        if state.is_processed(unique_id):
            continue

        logger.info(f"Processing new job: {job.title} at {job.company} ({job.source})")

        # 2. Summarize and Categorize with Local LLM
        summary_data = llm.summarize_job(job.title, job.company, job.description)
        
        # Rate Limiting: Minor sleep for local stability
        time.sleep(1)

        if not summary_data:
            logger.warning(f"Skipping job {unique_id} due to LLM processing failure.")
            continue

        # Filter: Check if suitable for newbie/junior (<= 3 years)
        if not summary_data.get('is_suitable', False):
            req_exp = summary_data.get('experience_requirement', 'Unknown')
            logger.info(f"Skipping job {unique_id} - Not suitable for junior level (Required: {req_exp} years).")
            state.mark_as_processed(unique_id)
            skipped_count += 1
            continue

        # 3. Add to Google Calendar
        success = calendar.add_job_event(
            job_title=job.title,
            company=job.company,
            summary_data=summary_data,
            link=job.link
        )

        if success:
            # 4. Send Discord Notification
            notifier.send_job_notification(
                job_title=job.title,
                company=job.company,
                summary_data=summary_data,
                link=job.link
            )
            
            # Collect for daily report
            suitable_jobs.append({
                'title': job.title,
                'company': job.company,
                'link': job.link,
                'source': job.source,
                'summary_data': summary_data
            })
            
            state.mark_as_processed(unique_id)
            new_jobs_count += 1
            logger.info(f"Successfully processed {job.title} at {job.company}.")

    # 5. Generate Daily Report if new jobs found
    if new_jobs_count > 0:
        report_path = report_gen.generate_daily_report(suitable_jobs)
        logger.info(f"Daily report generated at: {report_path}")
    else:
        logger.info("No new suitable jobs found today. Skipping report generation.")

    logger.info(f"Job crawling completed. {new_jobs_count} new suitable jobs processed. {skipped_count} skipped.")

if __name__ == "__main__":
    main()
