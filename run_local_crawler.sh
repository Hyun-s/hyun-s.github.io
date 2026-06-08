#!/bin/bash

# AI Job Crawler Local Execution Script
# This script runs the crawler using your local Qwen LLM (VLM) and pushes results to GitHub.

# 1. 필수 파일 체크
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found."
    echo "Please create a .env file based on .env.example"
    exit 1
fi

echo "✅ Environment check complete (.env found)"

# 2. 로컬 VLM(Ollama 등) 서버가 떠있는지 간단히 확인
if ! curl -s http://localhost:8000/v1/models > /dev/null; then
    echo "⚠️ Warning: Local LLM server at localhost:8000 might not be running or responding."
    echo "Make sure your Qwen3.5 VLM is running via docker-compose."
fi

# 3. 크롤러 실행 (Git Push는 main.py 내부에서 처리됨)
echo "🚀 Starting Local Job Crawler (with VLM support)..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/scripts/job_crawler
python3 scripts/job_crawler/main.py

echo "✅ Crawler execution finished. Check logs for details."
