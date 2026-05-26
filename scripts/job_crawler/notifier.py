import requests
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class DiscordNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_job_notification(self, job_title: str, company: str, summary_data: Dict, link: str):
        if not self.webhook_url:
            logger.warning("Discord Webhook URL is not set. Skipping notification.")
            return

        # Prepare Discord Embed message for a professional look
        embed = {
            "title": f"🚀 새로운 AI 채용 공고: {company}",
            "url": link,
            "color": 3447003, # Blue color
            "fields": [
                {
                    "name": "📌 포지션",
                    "value": job_title,
                    "inline": True
                },
                {
                    "name": "📅 마감일",
                    "value": summary_data.get("deadline") or "상시 채용",
                    "inline": True
                },
                {
                    "name": "📝 직군 요약",
                    "value": summary_data.get("role", "N/A"),
                    "inline": False
                },
                {
                    "name": "⭐ 우대사항",
                    "value": "\n".join([f"- {p}" for p in summary_data.get("preferences", [])[:5]]) or "내용 없음",
                    "inline": False
                },
                {
                    "name": "💡 핵심 요약",
                    "value": summary_data.get("summary", "N/A"),
                    "inline": False
                }
            ],
            "footer": {
                "text": "AI Job Crawler | GitHub Actions"
            }
        }

        payload = {
            "embeds": [embed]
        }

        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            logger.info(f"Discord notification sent for {job_title}")
            return True
        except Exception as e:
            logger.error(f"Failed to send Discord notification: {e}")
            return False
