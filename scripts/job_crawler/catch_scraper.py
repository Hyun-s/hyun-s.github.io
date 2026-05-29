import requests
import logging
import re
import json
from bs4 import BeautifulSoup
from typing import List, Optional, Dict, Any
from datetime import datetime
from job_models import JobInfo

logger = logging.getLogger(__name__)

class CatchScraper:
    BASE_URL = "https://www.catch.co.kr"
    CALENDAR_URL = "https://www.catch.co.kr/NCS/RecruitCalendar/Month"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': '1'
        })

    def _parse_nuxt_state(self, html: str) -> Optional[Dict[str, Any]]:
        """Extract and parse window.__NUXT__ from HTML"""
        logger.info("Attempting to parse NUXT state...")
        script_match = re.search(r'<script.*?>window\.__NUXT__=(.*?);?</script>', html, re.DOTALL)
        if not script_match:
            script_match = re.search(r'window\.__NUXT__=(.*?);?$', html, re.MULTILINE | re.DOTALL)
            
        if not script_match:
            logger.error("Could not find window.__NUXT__ state in HTML")
            return None
        
        js_code = script_match.group(1).strip()
        try:
            idx = js_code.rfind(")(")
            if idx == -1: idx = js_code.rfind("}(")
            if idx == -1: return None
            
            args_val_part = js_code[js_code.find("(", idx) + 1:]
            while args_val_part.endswith(')') or args_val_part.endswith(';'):
                args_val_part = args_val_part[:-1].strip()
            
            names_match = re.search(r'function\s*\((.*?)\)\s*\{', js_code)
            if not names_match: return None
            arg_names = [a.strip() for a in names_match.group(1).split(',')]
            
            args_val_part = args_val_part.replace('undefined', 'null').replace('void 0', 'null')
            try:
                arg_values = json.loads(f"[{args_val_part}]")
            except:
                import csv
                from io import StringIO
                reader = csv.reader(StringIO(args_val_part), quotechar='"', delimiter=',', skipinitialspace=True)
                arg_values = next(reader)
            
            mapping = dict(zip(arg_names, arg_values))
            body_start_idx = js_code.find("{")
            body_str = js_code[body_start_idx : idx + 1] 
            
            return {"mapping": mapping, "body": body_str}
        except Exception as e:
            logger.error(f"Error parsing NUXT JS: {e}")
            return None

    def crawl_all_jobs(self) -> List[JobInfo]:
        """Main crawling logic using NUXT state with batching and delays"""
        logger.info(f"Catch: Fetching recruitment calendar from {self.CALENDAR_URL}")
        try:
            import time
            import random
            
            # Initial home visit to look natural
            try: self.session.get(self.BASE_URL, timeout=10)
            except: pass
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(self.CALENDAR_URL, timeout=15)
            response.raise_for_status()
            
            parsed = self._parse_nuxt_state(response.text)
            if not parsed: return []
            
            mapping = parsed["mapping"]
            body = parsed["body"]
            
            month_match = re.search(r'recruitMonth:\{(.*?)\},[a-zA-Z_$][0-9a-zA-Z_$]*:', body, re.DOTALL)
            if not month_match: month_match = re.search(r'recruitMonth:\{(.*?)\},', body, re.DOTALL)
            if not month_match: return []
            
            month_data_str = month_match.group(1)
            all_jobs = []
            seen_ids = set()
            
            date_entries = re.split(r'("20\d{2}-\d{2}-\d{2}":)', month_data_str)
            current_date = None
            
            for entry in date_entries:
                if re.match(r'"20\d{2}-\d{2}-\d{2}":', entry):
                    current_date = entry.strip('":')
                    continue
                
                # All jobs from the calendar
                if current_date and entry.strip():
                    job_objs = re.findall(r'\{(.*?)\}', entry)
                    for obj_str in job_objs:
                        id_match = re.search(r'RecruitID:(\d+|[a-zA-Z_$][0-9a-zA-Z_$]*)', obj_str)
                        comp_match = re.search(r'CompName:(".*?"|[a-zA-Z_$][0-9a-zA-Z_$]*)', obj_str)
                        
                        if id_match and comp_match:
                            raw_id = id_match.group(1)
                            job_id = str(mapping.get(raw_id, raw_id))
                            if job_id in seen_ids: continue
                            seen_ids.add(job_id)
                            
                            raw_comp = comp_match.group(1)
                            company = raw_comp.strip('"') if raw_comp.startswith('"') else str(mapping.get(raw_comp, raw_comp))
                            
                            logger.info(f"Fetching job {len(all_jobs)+1}: {company} ({job_id})")
                            detail_url = f"{self.BASE_URL}/NCS/RecruitInfoDetails/{job_id}"
                            
                            time.sleep(random.uniform(5, 12)) # More conservative delay
                            job_info = self.get_job_detail(detail_url, job_id, company)
                            
                            if not job_info:
                                # Fallback: Use company name as title if fetch failed
                                # This ensures the calendar is at least populated with companies
                                job_info = JobInfo(
                                    id=job_id,
                                    title=f"{company} 채용", # Placeholder title
                                    company=company,
                                    description="상세 내용을 가져올 수 없습니다. 링크를 확인하세요.",
                                    deadline=current_date, # Use the date from calendar
                                    link=detail_url,
                                    source="Catch",
                                    start_date=current_date,
                                    end_date=current_date
                                )
                            
                            if job_info:
                                all_jobs.append(job_info)
            
            logger.info(f"Successfully processed {len(all_jobs)} jobs from Catch")
            return all_jobs
        except Exception as e:
            logger.error(f"Error crawling Catch: {e}")
            return []

    def get_job_detail(self, url: str, job_id: str, company: str) -> Optional[JobInfo]:
        """Fetch job details with enhanced headers to bypass blocks"""
        import time
        import random
        
        # Enhanced headers for detail page
        headers = self.session.headers.copy()
        headers.update({
            'Referer': self.CALENDAR_URL,
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'document',
        })
        
        for attempt in range(2):
            try:
                response = self.session.get(url, headers=headers, timeout=10)
                
                # If blocked, try to sleep longer and log it
                if response.status_code == 403:
                    logger.warning(f"403 Blocked for {url}. Attempt {attempt+1}")
                    time.sleep(random.uniform(20, 40))
                    continue
                    
                if response.status_code == 404:
                    # Try alternate path
                    url = f"{self.BASE_URL}/RecruitInfoDetails/{job_id}"
                    continue
                
                response.raise_for_status()
                if "페이지는 사라졌거나" in response.text: return None
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract Title
                title_tag = soup.select_one('.tit') or soup.select_one('h2')
                if not title_tag:
                    # Try to get from <title> tag
                    page_title = soup.title.string if soup.title else ""
                    title = page_title.split('|')[0].strip() if '|' in page_title else page_title
                else:
                    title = title_tag.get_text(strip=True)
                
                title = title or "채용 공고"
                
                date_text = ""
                date_info = soup.select_one('.rec_term') or soup.select_one('.date')
                if date_info: date_text = date_info.get_text(strip=True)
                
                start_date, end_date = self._parse_dates(date_text)
                
                # Extract Description (JD) - this is what LLM needs
                desc_tag = soup.select_one('.view_cont') or soup.select_one('.rec_view') or soup.select_one('.job_cont')
                description = ""
                if desc_tag:
                    description = desc_tag.get_text(strip=True, separator='\n')
                
                # If BS4 fails, try NUXT state
                if len(description) < 100:
                    logger.info(f"BS4 JD too short, checking NUXT state for {job_id}")
                    script_match = re.search(r'window\.__NUXT__=(.*?);?</script>', response.text, re.DOTALL)
                    if script_match:
                        js_code = script_match.group(1).strip()
                        # Find all Korean strings that look like HTML or JD content
                        strings = re.findall(r'"([^"]*?[\uac00-\ud7af][^"]*?)"', js_code)
                        if strings:
                            jd_kws = ["자격", "우대", "업무", "절차", "모집", "요건"]
                            candidates = [s for s in strings if any(kw in s for kw in jd_kws)]
                            candidates.sort(key=len, reverse=True)
                            if candidates:
                                best = candidates[0]
                                try:
                                    # Handle unicode escapes and HTML tags
                                    best = best.encode().decode('unicode-escape')
                                    # Basic HTML tag removal
                                    best = re.sub(r'<[^>]+>', '\n', best)
                                    description = best.strip()
                                except:
                                    description = candidates[0]
                
                if len(description) < 50:
                    logger.warning(f"Description too short ({len(description)}) for job {job_id}")
                else:
                    logger.info(f"Successfully retrieved JD ({len(description)} chars) for {company}")

                return JobInfo(job_id, title, company, description, end_date, url, "Catch", start_date, end_date)
            except Exception as e:
                logger.error(f"Attempt {attempt+1} failed for {job_id}: {e}")
                time.sleep(5)
        return None

    def _parse_dates(self, date_text: str):
        today = datetime.now().strftime("%Y-%m-%d")
        start, end = today, today
        try:
            dates = re.findall(r'(\d{4}[.\-/]\d{2}[.\-/]\d{2})', date_text)
            if len(dates) >= 2:
                start, end = [d.replace('.', '-') for d in dates[:2]]
            elif len(dates) == 1:
                end = dates[0].replace('.', '-')
        except: pass
        return start, end
