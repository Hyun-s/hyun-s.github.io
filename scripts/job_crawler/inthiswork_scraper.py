import requests
import logging
from typing import List, Optional
from bs4 import BeautifulSoup
from base_scraper import BaseScraper
from job_models import JobInfo

logger = logging.getLogger(__name__)

class InThisWorkScraper(BaseScraper):
    BASE_URL = "https://inthiswork.com"
    
    def __init__(self):
        super().__init__()

    def search_jobs(self, keywords: List[str], limit: int = 20) -> List[JobInfo]:
        all_jobs = []
        for keyword in keywords:
            # WordPress 검색 기능 활용
            url = f"{self.BASE_URL}/?s={keyword}"
            logger.info(f"InThisWork: Searching for '{keyword}' via {url}")
            
            try:
                response = requests.get(url, headers=self.headers, timeout=15)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 공고 아이템 래퍼 찾기 (Avada 테마)
                items = soup.select('.fusion-post-wrapper') or soup.select('.fusion-post-content-wrapper')
                
                count = 0
                for item in items:
                    if count >= limit: break
                    
                    link_elem = item.select_one('.entry-title a')
                    if not link_elem: continue
                    
                    full_title = link_elem.get_text(strip=True)
                    link = link_elem.get('href')
                    if '/archives/' not in link: continue
                    
                    job_id = link.rstrip('/').split('/')[-1]
                    
                    # 제목에서 회사명과 직무 분리 (형식: 회사명｜직무명)
                    if '｜' in full_title:
                        company, title = full_title.split('｜', 1)
                    else:
                        company, title = "InThisWork", full_title
                    
                    # 간단한 설명 (리스트 페이지에 있는 텍스트)
                    desc_elem = item.select_one('.fusion-post-content') or item.select_one('.entry-content')
                    description = desc_elem.get_text('\n', strip=True) if desc_elem else "상세 페이지 참조"
                    
                    all_jobs.append(JobInfo(
                        id=job_id,
                        title=title.strip(),
                        company=company.strip(),
                        description=description,
                        deadline=None,
                        link=link,
                        source="InThisWork"
                    ))
                    count += 1
                    
            except Exception as e:
                logger.error(f"Error searching InThisWork for '{keyword}': {e}")
                
        return all_jobs

    def get_job_detail(self, job_id: str) -> Optional[JobInfo]:
        # 필요시 상세 페이지를 다시 방문하여 더 긴 텍스트를 가져올 수 있습니다.
        return None
