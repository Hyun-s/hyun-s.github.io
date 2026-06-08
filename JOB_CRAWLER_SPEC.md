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
- **Catch (`catch_scraper.py`):** Primary source. Parses NUXT state and HTML. Now extracts both text and **Image URLs** (resolving missing context from image-based job postings) with dynamic delay to prevent blocking.
- **Wanted (`wanted_scraper.py`):** Uses unofficial v4 API for precise structured data.
- **InThisWork (`inthiswork_scraper.py`):** Parses WordPress search results using `BeautifulSoup4`.

### 🧠 AI Analysis (Local VLM)
- **Engine:** Local **Qwen-35-122B (VLM supported)** running via Docker (vLLM) at `localhost:8000`.
- **Logic (`llm_processor.py`):**
    - **Vision Processing:** Resizes images to prevent `400 Bad Request` and passes them to the VLM via Base64 to extract text exactly as written.
    - **Domain Detection:** Categorizes into Vision, LLM, Diffusion, Agentic AI, etc.
    - **Strict Filtering:** Identifies and completely rejects non-AI roles or postings with insufficient information (e.g., "판단 불가").
    - **Junior Suitability:** Identifies if a role requires ≤ 3 years of experience. Jobs requiring > 3 years are isolated.
    - **Precise Information Extraction:** Extracts the exact recruitment period string (e.g., "2026.05.26 ~ 2026.06.25"), exact experience requirements, key requirements, and preferences.

### 📢 Multi-Channel Distribution
1.  **Google Calendar:** Creates deadline-based events with full summaries.
2.  **Discord:** Sends rich Embed notifications with domain-specific labels.
3.  **Hugo Publisher (`report_generator.py`):** 
    - **Active Junior Jobs:** Generates the main daily `.md` report, displaying jobs in categorized toggle (`<details>`) sections.
    - **Experienced Jobs (3년 초과):** Isolated into a separate hidden `.md` file, accessible only via a link at the top of the main report.
    - **Closed Jobs (오늘 마감):** Isolated into a separate hidden `.md` file to highlight urgency without cluttering the main active list.
    - Jobs closed *before* today are permanently excluded.
4.  **Local Sync:** Crontab-based automatic synchronization to local notes.

## 4. Execution Workflow
1.  **Local Run (`run_crawl.sh`):**
    - Triggered manually or by local scheduler.
    - Verifies `.env` and VLM server status.
    - Executes `main.py` -> Processes jobs (Text + Vision) -> `git push` results automatically.
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
*Last Updated: 2026-06-09 by Gemini CLI Agent*
