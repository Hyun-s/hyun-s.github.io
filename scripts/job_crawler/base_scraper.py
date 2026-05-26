from typing import List, Optional
from job_models import JobInfo

class BaseScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }

    def search_jobs(self, keywords: List[str], limit: int = 20) -> List[JobInfo]:
        """
        주어진 키워드로 채용 공고를 검색하여 JobInfo 리스트를 반환합니다.
        각 서브클래스에서 구현해야 합니다.
        """
        raise NotImplementedError("Subclasses must implement search_jobs")

    def get_job_detail(self, job_id: str) -> Optional[JobInfo]:
        """
        공고 상세 정보를 가져와 JobInfo 객체를 반환합니다.
        각 서브클래스에서 구현해야 합니다.
        """
        raise NotImplementedError("Subclasses must implement get_job_detail")
