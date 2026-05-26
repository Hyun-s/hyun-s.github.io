#!/bin/bash

# AI Job Crawler Local Execution Script
# This script runs the crawler using your local Qwen LLM and pushes results to GitHub.

# 1. 필수 파일 체크
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found."
    echo "Please create a .env file based on .env.example"
    exit 1
fi

echo "✅ Environment check complete (.env found)"

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
