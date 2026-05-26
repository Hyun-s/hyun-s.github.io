import os
import json
import logging
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List, Dict

logger = logging.getLogger(__name__)

class CalendarManager:
    def __init__(self, credentials_json: str, calendar_id: str):
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        self.calendar_id = calendar_id
        
        try:
            creds_dict = json.loads(credentials_json)
            self.creds = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=self.scopes
            )
            self.service = build('calendar', 'v3', credentials=self.creds)
        except Exception as e:
            logger.error(f"Failed to initialize Google Calendar client: {e}")
            raise

    def add_job_event(self, job_title: str, company: str, summary_data: Dict, link: str):
        """
        summary_data example: 
        { "role": "...", "deadline": "2026-05-30", "preferences": ["A", "B"], "summary": "..." }
        """
        deadline = summary_data.get("deadline")
        if not deadline:
            # If no deadline, set it to 2 weeks from now as a placeholder or just skip
            # For this requirement, we'll set it to 14 days from now if not found
            deadline = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        # Build description
        desc_parts = [
            f"🏢 회사: {company}",
            f"🔗 공고 링크: {link}",
            f"📝 직군 요약: {summary_data.get('role', 'N/A')}",
            "\n⭐ 우대사항:",
        ]
        for pref in summary_data.get("preferences", []):
            desc_parts.append(f"- {pref}")
        
        desc_parts.append(f"\n💡 핵심 요약:\n{summary_data.get('summary', 'N/A')}")
        
        description = "\n".join(desc_parts)
        
        event = {
            'summary': f"[채용 마감] {company} - {job_title}",
            'description': description,
            'start': {
                'date': deadline,
            },
            'end': {
                'date': deadline, # All-day event
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24 * 60}, # 1 day before
                    {'method': 'email', 'minutes': 2 * 24 * 60}, # 2 days before
                ],
            },
        }

        try:
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            logger.info(f"Event created: {event.get('htmlLink')}")
            return True
        except Exception as e:
            logger.error(f"Error creating calendar event: {e}")
            return False

class StateManager:
    def __init__(self, file_path: str = "processed_jobs.json"):
        self.file_path = file_path
        self.processed_ids = self._load()

    def _load(self) -> List[str]:
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading state: {e}")
        return []

    def is_processed(self, job_id: str) -> bool:
        return job_id in self.processed_ids

    def mark_as_processed(self, job_id: str):
        if job_id not in self.processed_ids:
            self.processed_ids.append(job_id)
            self._save()

    def _save(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.processed_ids, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {e}")
