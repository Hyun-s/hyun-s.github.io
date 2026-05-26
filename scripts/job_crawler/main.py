import os
import logging
import time
from dotenv import load_dotenv
from wanted_scraper import WantedScraper
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
    load_dotenv()
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gcp_credentials = os.getenv("GCP_CREDENTIALS")
    calendar_id = os.getenv("CALENDAR_ID")
    discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not all([gemini_api_key, gcp_credentials, calendar_id]):
        logger.error("Missing required environment variables. Please check GEMINI_API_KEY, GCP_CREDENTIALS, and CALENDAR_ID.")
        return

    # Initialize components
    scraper = WantedScraper()
    llm = LLMProcessor(gemini_api_key)
    calendar = CalendarManager(gcp_credentials, calendar_id)
    notifier = DiscordNotifier(discord_webhook_url)
    state = StateManager("processed_jobs.json")
    
    # Paths relative to the repo root (running from root or scripts/job_crawler)
    # If running from root: content/job-report
    # If running from scripts/job_crawler: ../../content/job-report
    # We'll assume it runs from repo root as per GitHub Action
    report_gen = ReportGenerator("content/job-report")

    keywords = ["AI Research", "Machine Learning Scientist", "Deep Learning Research", "LLM Engineer", "Computer Vision Engineer"]
    logger.info(f"Starting job crawl for keywords: {keywords}")

    # 1. Search for jobs
    jobs = scraper.search_jobs(keywords, limit=20)
    logger.info(f"Found {len(jobs)} potential jobs.")

    new_jobs_count = 0
    suitable_jobs = []
    skipped_count = 0

    for job in jobs:
        # Check if already processed
        if state.is_processed(job.id):
            continue

        logger.info(f"Processing new job: {job.title} at {job.company}")

        # 2. Summarize and Categorize with Local LLM
        summary_data = llm.summarize_job(job.title, job.company, job.description)
        
        # Rate Limiting: Minor sleep for local stability
        time.sleep(1)

        if not summary_data:
            logger.warning(f"Skipping job {job.id} due to LLM processing failure.")
            continue

        # Filter: Check if suitable for newbie/junior (<= 3 years)
        if not summary_data.get('is_suitable', False):
            req_exp = summary_data.get('experience_requirement', 'Unknown')
            logger.info(f"Skipping job {job.id} - Not suitable for junior level (Required: {req_exp} years).")
            # We still mark it as processed to avoid re-checking
            state.mark_as_processed(job.id)
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
                'summary_data': summary_data
            })
            
            state.mark_as_processed(job.id)
            new_jobs_count += 1
            logger.info(f"Successfully processed {job.title} at {job.company}.")

    # 5. Generate Daily Report if new jobs found
    if new_jobs_count > 0:
        report_path = report_gen.generate_daily_report(suitable_jobs)
        logger.info(f"Daily report generated at: {report_path}")
    else:
        logger.info("No new suitable jobs found today. Skipping report generation.")

    logger.info(f"Job crawling completed. {new_jobs_count} new suitable jobs processed.")

if __name__ == "__main__":
    main()
