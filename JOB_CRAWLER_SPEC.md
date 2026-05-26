# 📑 AI Job Crawler & Multi-Channel Reporting System Specification

This document serves as the official technical specification for the AI Job Crawler system. It is designed to provide all necessary context for future AI agents or developers to maintain and extend the system.

## 1. System Overview
The system automates the lifecycle of AI job hunting: discovery, analysis, filtering, and reporting. It targets specific research and engineering roles, uses LLMs for categorization, and distributes findings across multiple channels.

## 2. Technical Architecture
- **Execution:** GitHub Actions (Ubuntu-latest, Python 3.11)
- **Deployment:** GitHub Pages (Hugo-based static site)
- **Scheduling:** Daily at 09:00 KST (`0 0 * * *` UTC)
- **State Management:** Local JSON file (`processed_jobs.json`) tracked via Git to ensure idempotency.

## 3. Directory Structure
```text
scripts/job_crawler/
├── main.py             # Orchestrator: manages the overall flow
├── wanted_scraper.py   # Scraper: fetches raw data from Wanted API
├── llm_processor.py    # AI Engine: summarizes, categorizes, and filters
├── calendar_manager.py # Integrator: handles Google Calendar API
├── notifier.py         # Integrator: handles Discord Webhooks
├── report_generator.py # Publisher: creates Hugo Markdown reports
└── requirements.txt    # Dependencies
```

## 4. Module Deep Dive

### 🛰️ Wanted Scraper (`wanted_scraper.py`)
- **API Endpoint:** `https://www.wanted.co.kr/api/v4/jobs`
- **Method:** GET with specific headers (User-Agent, Referer) to emulate a browser.
- **Filtering:** Filters by `tag_type_ids: 518` (Development) and custom keywords.
- **Data Model:** `JobInfo` dataclass (id, title, company, description, deadline, link).

### 🧠 LLM Processor (`llm_processor.py`)
- **Model:** `gemini-1.5-flash` with fallback to `gemini-1.5-flash-latest` and `gemini-pro`.
- **Functionality:**
    - **Classification:** Categorizes into technical domains (LLM, Vision, etc.) and job types (Compression, Agent, etc.).
    - **Junior Filtering:** Logic specifically tuned to detect roles suitable for Master's graduates with ≤ 3 years of experience.
- **Output Schema (JSON):**
  ```json
  {
    "domain": "Vision",
    "job_type": "모델 경량화(Compression)",
    "role_summary": "...",
    "experience_requirement": 1,
    "is_suitable": true,
    "key_requirements": ["..."],
    "preferences": ["..."],
    "summary": "..."
  }
  ```

### 📢 Distribution Channels
1.  **Google Calendar:** Creates all-day events on the job's deadline date. Includes summaries and links in the description.
2.  **Discord:** Sends rich Embed messages with color-coded status and categorized fields.
3.  **Hugo Website:** Generates `content/job-report/YYYY-MM-DD.md`.
4.  **Local Sync:** Automates `git pull` via local crontab to sync reports to `/home/hyuns/notes/Hyuns/Job_prepare/`.

## 5. Security & Environment Variables
The following secrets MUST be configured in the GitHub Repository:
- `GEMINI_API_KEY`: Google AI Studio API Key.
- `GCP_CREDENTIALS`: Full JSON of the GCP Service Account Key.
- `CALENDAR_ID`: The target Google Calendar ID (Shared with the Service Account).
- `DISCORD_WEBHOOK_URL`: The Discord channel webhook URL.

## 6. Maintenance & Extension
- **Adding Keywords:** Update the `keywords` list in `main.py`.
- **Adjusting Filtering:** Modify the `is_suitable` criteria in the `LLMProcessor` prompt.
- **New Sources:** Create a new scraper class following the `JobInfo` interface and integrate it into `main.py`.
- **UI Changes:** Modify `assets/css/style.css` (look for `/* Job Report Styles */`) and `layouts/_default/list.html`.

## 7. Local Setup (One-time)
To sync reports locally, run:
```bash
ln -s /home/hyuns/hyun-s.github.io/content/job-report /home/hyuns/notes/Hyuns/Job_prepare/daily_reports
(crontab -l 2>/dev/null; echo "5 9 * * * cd /home/hyuns/hyun-s.github.io && /usr/bin/git pull origin main") | crontab -
```

---
*Created by Gemini CLI Agent - 2026-05-26*
