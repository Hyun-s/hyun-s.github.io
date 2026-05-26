import requests
import logging
import json
from typing import List, Optional
from base_scraper import BaseScraper
from job_models import JobInfo

logger = logging.getLogger(__name__)

class CatchScraper(BaseScraper):
    BASE_URL = "https://www.catch.co.kr"
    # 캐치 채용 검색 API (분석 기반 예상 경로)
    API_URL = "https://www.catch.co.kr/api/v1/recruitment/list" 
    
    def __init__(self):
        super().__init__()
        self.headers.update({
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        })

    def search_jobs(self, keywords: List[str], limit: int = 20) -> List[JobInfo]:
        all_jobs = []
        for keyword in keywords:
            # 캐치 웹사이트 검색 파라미터 (분석 기반)
            params = {
                "Keyword": keyword,
                "Order": "1", # 최신순
                "PageSize": limit,
                "CurrentPage": "1"
            }
            
            try:
                # 실제 캐치는 /NCS/RecruitSearchAjax 등에서 데이터를 가져올 수 있음
                search_url = f"{self.BASE_URL}/NCS/RecruitSearchAjax"
                response = requests.get(search_url, params=params, headers=self.headers)
                
                # 만약 JSON이 아니라 HTML을 반환한다면 BeautifulSoup 파싱으로 전환해야 함
                if 'application/json' in response.headers.get('Content-Type', ''):
                    data = response.json()
                    for item in data.get("List", []):
                        job_id = str(item.get("RecruitNo"))
                        all_jobs.append(self._parse_item(item))
                else:
                    # HTML 파싱 로직 (필요시 추가)
                    pass
                    
            except Exception as e:
                logger.error(f"Error searching Catch for '{keyword}': {e}")
                
        return all_jobs

    def _parse_item(self, item: dict) -> JobInfo:
        job_id = str(item.get("RecruitNo"))
        return JobInfo(
            id=job_id,
            title=item.get("Title"),
            company=item.get("CompName"),
            description="상세 내용은 링크 참조 (캐치는 상세 페이지 파싱 필요)",
            deadline=item.get("EndDate"),
            link=f"{self.BASE_URL}/Recruit/RecruitDetail/{job_id}",
            source="Catch"
        )

    def get_job_detail(self, job_id: str) -> Optional[JobInfo]:
        # 캐치 상세 페이지는 복잡한 HTML 구조를 가짐
        # 여기서는 기본 정보만 반환하거나 BeautifulSoup으로 본문 추출
        return None
