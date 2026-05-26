import requests
import logging
from typing import List, Optional
from base_scraper import BaseScraper
from job_models import JobInfo

logger = logging.getLogger(__name__)

class WantedScraper(BaseScraper):
    BASE_URL = "https://www.wanted.co.kr/api/v4/jobs"
    
    def __init__(self):
        super().__init__()
        self.headers.update({
            "Referer": "https://www.wanted.co.kr/wdlist/518",
            "Accept": "application/json"
        })

    def search_jobs(self, keywords: List[str], limit: int = 20) -> List[JobInfo]:
        all_jobs = []
        for keyword in keywords:
            params = {
                "country": "kr",
                "tag_type_ids": "518", # 개발
                "job_sort": "job.latest_order",
                "locations": "all",
                "years": "-1",
                "keyword": keyword,
                "limit": limit,
                "offset": 0
            }
            
            try:
                response = requests.get(self.BASE_URL, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                jobs = data.get("data", [])
                for job in jobs:
                    job_id = str(job.get("id"))
                    job_detail = self.get_job_detail(job_id)
                    if job_detail:
                        all_jobs.append(job_detail)
                
            except Exception as e:
                logger.error(f"Error searching Wanted for keyword '{keyword}': {e}")
                
        return all_jobs

    def get_job_detail(self, job_id: str) -> Optional[JobInfo]:
        url = f"{self.BASE_URL}/{job_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json().get("job", {})
            
            detail = data.get("detail", {})
            description = f"### 주요업무\n{detail.get('main_tasks')}\n\n### 자격요건\n{detail.get('requirements')}\n\n### 우대사항\n{detail.get('preferred_points')}"
            
            return JobInfo(
                id=job_id,
                title=data.get("position"),
                company=data.get("company", {}).get("name"),
                description=description,
                deadline=data.get("due_time"),
                link=f"https://www.wanted.co.kr/wd/{job_id}",
                source="Wanted"
            )
        except Exception as e:
            logger.error(f"Error getting Wanted job detail for {job_id}: {e}")
            return None
