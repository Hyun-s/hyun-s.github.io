# 📑 AI Job Intelligence & Personal Portfolio System Specification

This document serves as the official technical specification for the integrated portfolio and AI job intelligence system.

## 1. System Overview
The system combines a professional research portfolio (Hugo) with an automated AI job intelligence engine. It automates the discovery, analysis, filtering, and reporting of AI-related roles, specifically targeting junior-level (≤ 3 years) positions suitable for a Master's graduate.

## 2. Website Architecture (Hugo)
- **Framework:** Hugo (Static Site Generator)
- **Design:** Professional Minimalist (Indigo & Slate theme)
- **Deployment:** Fully automated via GitHub Actions (`deploy.yml`) to GitHub Pages.
- **Key Sections:**
    - **Home:** Research summary, LinkedIn integration, and CVPR 2026 highlights.
    - **CV:** Elegant timeline-based education and experience list.
    - **Calendar:** Interactive event manager using `localStorage`.
    - **Job Report:** Daily Markdown reports categorized by technical domain.

## 3. Intelligence Engine (Python 3.11)

### 🛰️ Data Collection (Multi-Source)
- **Wanted (`wanted_scraper.py`):** Uses unofficial v4 API for precise structured data.
- **InThisWork (`inthiswork_scraper.py`):** Parses WordPress search results using `BeautifulSoup4`.
- **Catch (`catch_scraper.py`):** Interacts with internal Ajax (POST) endpoints for real-time listings.

### 🧠 AI Analysis (Local LLM)
- **Engine:** Local **Qwen-35-122B** running via Docker (vLLM) at `localhost:8000`.
- **Logic (`llm_processor.py`):**
    - **Domain Detection:** Categorizes into Vision, LLM, Diffusion, Agentic AI, etc.
    - **Strict Filtering:** Identifies and rejects non-AI roles (Web/App dev).
    - **Junior Suitability:** Filters for roles requiring ≤ 3 years of experience.
    - **JSON Structuring:** Converts unstructured text into a common data schema.

### 📢 Multi-Channel Distribution
1.  **Google Calendar:** Creates deadline-based events with full summaries.
2.  **Discord:** Sends rich Embed notifications with domain-specific labels.
3.  **Hugo Publisher:** Generates daily `.md` files in `content/job-report/`.
4.  **Local Sync:** Crontab-based automatic synchronization to local notes.

## 4. Execution Workflow
1.  **Local Run (`run_local_crawler.sh`):**
    - Triggered manually or by local scheduler.
    - Loads secrets from `.env` via `python-dotenv`.
    - Executes `main.py` -> Processes jobs -> `git push` results.
2.  **CI/CD Trigger:**
    - GitHub receives the push -> `deploy.yml` triggers.
    - Hugo builds the site with new reports -> Site goes live.
3.  **Local Sync:**
    - Crontab (`5 9 * * *`) executes `git pull` -> Reports available in local notes.

## 5. Security & Maintenance
- **Environment Variables:** Managed via `.env` (ignored by Git). See `.env.example`.
- **State Management:** `processed_jobs.json` tracks unique `source_id` keys.
- **Dependencies:** Managed in `scripts/job_crawler/requirements.txt`.
- **Keywords:** Defined in `scripts/job_crawler/main.py`.

---
*Last Updated: 2026-05-27 by Gemini CLI Agent*
