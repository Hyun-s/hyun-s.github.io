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
        # InThisWork는 /talent-board/all 페이지에서 공고를 리스팅함
        # 특정 키워드로 검색 기능이 URL 파라미터로 명확하지 않을 경우 전체를 읽어서 필터링
        url = f"{self.BASE_URL}/talent-board/all"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 공고 리스트 아이템 찾기 (실제 클래스명은 사이트 분석 필요)
            # 여기서는 분석된 일반적인 패턴을 사용합니다.
            job_cards = soup.select('div.job-card') or soup.select('a[href^="/talent-board/"]')
            
            count = 0
            for card in job_cards:
                if count >= limit: break
                
                href = card.get('href') if card.name == 'a' else card.select_one('a').get('href')
                if not href or '/talent-board/' not in href: continue
                
                job_id = href.split('/')[-1]
                
                # 키워드 필터링 (제목에서 1차 필터링)
                title_text = card.get_text()
                if any(kw.lower() in title_text.lower() for kw in keywords):
                    detail = self.get_job_detail(job_id)
                    if detail:
                        all_jobs.append(detail)
                        count += 1
            
        except Exception as e:
            logger.error(f"Error searching InThisWork: {e}")
            
        return all_jobs

    def get_job_detail(self, job_id: str) -> Optional[JobInfo]:
        url = f"{self.BASE_URL}/talent-board/{job_id}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.select_one('h1').get_text(strip=True)
            company = soup.select_one('.company-name').get_text(strip=True) if soup.select_one('.company-name') else "InThisWork Company"
            
            # 본문 내용 추출
            content = soup.select_one('.job-description') or soup.select_one('article')
            description = content.get_text('\n', strip=True) if content else "상세 내용 없음"
            
            return JobInfo(
                id=job_id,
                title=title,
                company=company,
                description=description,
                deadline=None, # 마감일 정보가 본문에 포함된 경우가 많음 (LLM이 처리)
                link=url,
                source="InThisWork"
            )
        except Exception as e:
            logger.error(f"Error getting InThisWork detail for {job_id}: {e}")
            return None
