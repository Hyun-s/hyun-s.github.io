# AI Job Crawler

This system crawls job postings from various sources (primarily Catch.co.kr), classifies them using a local LLM, and populates a Hugo-based calendar and daily reports.

## Features
- **Catch.co.kr Integration**: Scrapes the monthly recruitment calendar.
- **AI Classification**: Uses a local Qwen3.5 LLM to categorize jobs (Vision, LLM, Research, etc.).
- **Deep Analysis**: Extracts role summaries, requirements, and suitability for AI-related roles.
- **Multi-channel Notifications**: Sends alerts to Discord and adds events to Google Calendar.
- **Hugo Integration**: Outputs data to `data/jobs.json` for the static site.
- **Daily Reports**: Generates Markdown reports in `content/job-report/`.

## Setup

### 1. Requirements
- Python 3.8+
- Local LLM running (compatible with OpenAI API, e.g., via Docker Compose)
- Hugo (for site generation)

### 2. Installation
```bash
cd scripts/job_crawler
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_key_if_needed
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
CALENDAR_ID=your_google_calendar_id
GCP_CREDENTIALS='{"type": "service_account", ...}'
```

Edit `data/job-categories.toml` to customize categories and keywords.

### 4. Manual Overrides
If the LLM misclassifies a job, you can manually override it in `data/job-overrides.json`:
```json
{
  "catch_311441": {
    "category": "vision",
    "skills": ["Python", "PyTorch"],
    "subcategories": ["object-detection"]
  }
}
```

## Running the Crawler
```bash
python scripts/job_crawler/main.py
```

## Deployment
The crawler is designed to be run via cron (see `.cron/job_crawler.sh`). It automatically commits and pushes changes to `data/jobs.json`, which triggers the Hugo deployment workflow.
