import requests
import logging
import json
from typing import List, Optional
from base_scraper import BaseScraper
from job_models import JobInfo

logger = logging.getLogger(__name__)

class CatchScraper(BaseScraper):
    BASE_URL = "https://www.catch.co.kr"
    # 캐치 채용 검색 AJAX API (POST 방식)
    API_URL = "https://www.catch.co.kr/NCS/RecruitSearchAjax"
    
    def __init__(self):
        super().__init__()
        self.headers.update({
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.catch.co.kr/NCS/RecruitSearch"
        })

    def search_jobs(self, keywords: List[str], limit: int = 20) -> List[JobInfo]:
        all_jobs = []
        for keyword in keywords:
            logger.info(f"Catch: Searching for '{keyword}' via {self.API_URL}")
            
            # 캐치 POST 파라미터
            # RecruitType: 1(신입), 2(경력), 3(인턴), 4(경력무관)
            # 여기서는 우선 키워드 기반으로 넓게 검색합니다.
            data = {
                "Keyword": keyword,
                "Order": "1", # 1: 최신순
                "PageSize": str(limit),
                "CurrentPage": "1"
            }
            
            try:
                response = requests.post(self.API_URL, headers=self.headers, data=data, timeout=15)
                response.raise_for_status()
                
                # 캐치 API는 보통 HTML 조각(Snippet)을 반환하는 경우가 많습니다.
                # 만약 JSON이라면 아래와 같이 처리:
                try:
                    json_data = response.json()
                    items = json_data.get("List", [])
                    for item in items:
                        all_jobs.append(self._parse_json_item(item))
                except json.JSONDecodeError:
                    # HTML 조각을 반환할 경우 (현재 웹사이트 방식)
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 캐치 검색 결과 리스트 아이템 찾기
                    # 보통 'li' 태그 안에 정보가 들어있습니다.
                    list_items = soup.select('li')
                    for li in list_items:
                        info = self._parse_html_item(li)
                        if info:
                            all_jobs.append(info)
                            
            except Exception as e:
                logger.error(f"Error searching Catch for '{keyword}': {e}")
                
        return all_jobs

    def _parse_json_item(self, item: dict) -> JobInfo:
        job_id = str(item.get("RecruitNo"))
        return JobInfo(
            id=job_id,
            title=item.get("Title"),
            company=item.get("CompName"),
            description=f"마감일: {item.get('EndDate')}",
            deadline=item.get("EndDate"),
            link=f"{self.BASE_URL}/Recruit/RecruitDetail/{job_id}",
            source="Catch"
        )

    def _parse_html_item(self, li) -> Optional[JobInfo]:
        try:
            # 제목 및 링크 추출
            link_elem = li.select_one('.tit a') or li.select_one('a[href*="RecruitDetail"]')
            if not link_elem: return None
            
            title = link_elem.get_text(strip=True)
            href = link_elem.get('href')
            
            # ID 추출 (RecruitDetail/123456 형태)
            import re
            match = re.search(r'RecruitDetail/(\d+)', href)
            job_id = match.group(1) if match else href.split('/')[-1]
            
            # 회사명 추출
            company_elem = li.select_one('.comp') or li.select_one('.name')
            company = company_elem.get_text(strip=True) if company_elem else "Catch Employer"
            
            # 마감일 추출
            deadline_elem = li.select_one('.num_dday') or li.select_one('.date')
            deadline = deadline_elem.get_text(strip=True) if deadline_elem else None

            return JobInfo(
                id=job_id,
                title=title,
                company=company,
                description=f"상세 내용은 링크 참조. 마감일: {deadline}",
                deadline=deadline,
                link=f"{self.BASE_URL}/Recruit/RecruitDetail/{job_id}",
                source="Catch"
            )
        except Exception:
            return None

    def get_job_detail(self, job_id: str) -> Optional[JobInfo]:
        return None
