import requests
import logging
from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from job_models import JobInfo

logger = logging.getLogger(__name__)

class CatchScraper:
    BASE_URL = "https://www.catch.co.kr"
    CALENDAR_URL = "https://www.catch.co.kr/NCS/RecruitCalendar/Month"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def crawl_all_jobs(self) -> List[JobInfo]:
        """Main crawling logic for the monthly calendar"""
        logger.info(f"Catch: Fetching recruitment calendar from {self.CALENDAR_URL}")
        try:
            response = self.session.get(self.CALENDAR_URL, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all job links in the calendar grid
            # The structure might vary, but usually there are 'a' tags or list items in a calendar table
            job_links = soup.select('div.cal_list a[href*="RecruitDetail"]')
            
            seen_ids = set()
            all_jobs = []
            
            for link in job_links:
                href = link.get('href')
                if not href: continue
                
                # Full URL or relative path
                if href.startswith('/'):
                    detail_url = f"{self.BASE_URL}{href}"
                else:
                    detail_url = href
                
                # Extract ID for deduplication
                import re
                match = re.search(r'RecruitDetail/(\d+)', href)
                job_id = match.group(1) if match else href.split('/')[-1]
                
                if job_id in seen_ids: continue
                seen_ids.add(job_id)
                
                job_info = self.get_job_detail(detail_url, job_id)
                if job_info:
                    all_jobs.append(job_info)
                    
            return all_jobs
        except Exception as e:
            logger.error(f"Error crawling Catch calendar: {e}")
            return []

    def get_job_detail(self, url: str, job_id: str) -> Optional[JobInfo]:
        """Fetch detailed job info from the specific recruitment page"""
        logger.info(f"Catch: Fetching job details from {url}")
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            company = soup.select_one('.comp_name').get_text(strip=True) if soup.select_one('.comp_name') else "Catch Employer"
            title = soup.select_one('.tit').get_text(strip=True) if soup.select_one('.tit') else "Job Position"
            
            # Recruitment dates
            # These are often in a 'dl' or 'div' with specific classes
            # We need to find "접수기간" or similar
            date_info = soup.select_one('.rec_term') or soup.select_one('.date')
            date_text = date_info.get_text(strip=True) if date_info else ""
            
            # Parse dates (example format: 2026.05.01 ~ 2026.05.31)
            start_date, end_date = self._parse_dates(date_text)
            
            description = soup.select_one('.view_cont').get_text(strip=True) if soup.select_one('.view_cont') else ""
            
            return JobInfo(
                id=job_id,
                title=title,
                company=company,
                description=description,
                deadline=end_date, # Fallback/Compatibility
                link=url,
                source="Catch",
                start_date=start_date,
                end_date=end_date
            )
        except Exception as e:
            logger.error(f"Error fetching Catch job {job_id}: {e}")
            return None

    def _parse_dates(self, date_text: str):
        """Helper to parse recruitment period from text"""
        # Default to current if parsing fails
        today = datetime.now().strftime("%Y-%m-%d")
        start, end = today, today
        
        try:
            # Look for YYYY.MM.DD or YYYY-MM-DD
            import re
            dates = re.findall(r'(\d{4}[.\-/]\d{2}[.\-/]\d{2})', date_text)
            if len(dates) >= 2:
                start = dates[0].replace('.', '-')
                end = dates[1].replace('.', '-')
            elif len(dates) == 1:
                end = dates[0].replace('.', '-')
        except Exception:
            pass
            
        return start, end

    # Compatibility methods for main.py (if still using keywords)
    def search_jobs(self, keywords: List[str], limit: int = 20) -> List[JobInfo]:
        # For now, just crawl the calendar as it's the primary requirement
        return self.crawl_all_jobs()
