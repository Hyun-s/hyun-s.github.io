#!/bin/bash

# AI Job Crawler Local Execution Script
# This script runs the crawler using your local Qwen LLM and pushes results to GitHub.

# 1. 환경 변수 설정 (여기에 본인의 값을 입력하거나 .env 파일을 사용하세요)
# GCP_CREDENTIALS는 JSON 파일의 경로가 아니라 내용 자체여야 합니다.
export GEMINI_API_KEY="local" # 로컬 LLM이므로 무시됨
export CALENDAR_ID="본인의_캘린더_ID"
export DISCORD_WEBHOOK_URL="본인의_디스코드_웹훅_URL"
# GCP_CREDENTIALS는 scripts/job_crawler/main.py에서 os.getenv로 읽으므로 
# 실제 서비스 계정 JSON 내용을 환경변수에 넣어주어야 합니다.
# export GCP_CREDENTIALS='{...}' 

# 2. 가상환경 진입 (선택 사항)
# source venv/bin/activate

# 3. 크롤러 실행
echo "🚀 Starting Local Job Crawler..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/scripts/job_crawler
python3 scripts/job_crawler/main.py

# 4. 결과 커밋 및 푸시
echo "📝 Committing and Pushing results..."
git add processed_jobs.json content/job-report/
if git diff --staged --quiet; then
    echo "✅ No new jobs found."
else
    git commit -m "chore: update job reports via local LLM ($(date +'%Y-%m-%d'))"
    git push origin main
    echo "✅ Successfully pushed to GitHub."
fi
