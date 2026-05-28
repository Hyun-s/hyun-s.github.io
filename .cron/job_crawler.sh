#!/bin/bash
# .cron/job_crawler.sh

cd /home/hyuns/hyun-s.github.io
mkdir -p logs
# source venv/bin/activate  # If using virtualenv
python scripts/job_crawler/main.py >> logs/crawler.log 2>&1
