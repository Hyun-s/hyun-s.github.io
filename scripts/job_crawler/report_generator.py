import os
from datetime import datetime
from typing import List, Dict

class ReportGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_daily_report(self, jobs: List[Dict], experienced_jobs: List[Dict] = None) -> str:
        """
        jobs: List of dicts containing job details and LLM summary data.
        experienced_jobs: List of AI jobs filtered out due to experience limits.
        Returns the path of the generated report file.
        """
        if experienced_jobs is None:
            experienced_jobs = []
            
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
        file_time_str = now.strftime("%H%M")
        
        filename = f"{today_str}-{file_time_str}.md"
        filepath = os.path.join(self.output_dir, filename)

        # Hugo Frontmatter
        lines = [
            "---",
            f"title: \"Daily AI Job Report: {today_str} {time_str}\"",
            f"date: {now.isoformat()}",
            f"tags: [\"Job Report\", \"AI\", \"Research\"]",
            "categories: [\"Career\"]",
            "---",
            "",
            f"# 📅 AI Job Daily Report ({today_str} {time_str})",
            "",
            f"오늘 수집된 공고 중 석사 졸업 및 3년 이하 경력자에게 적합한 주니어급 AI 공고 **{len(jobs)}건**을 정리했습니다.",
            ""
        ]

        if not jobs:
            lines.append("오늘 새로 발견된 적합한 주니어급 AI 공고가 없습니다. ☕")
        else:
            # Group by Domain
            domain_map = {}
            for job in jobs:
                s_data = job.get('summary_data', {})
                domain = s_data.get('domain', 'Others')
                
                # Skip non-AI domains
                if domain.lower() in ['others', 'none-ai', 'none']:
                    continue
                    
                if domain not in domain_map:
                    domain_map[domain] = []
                domain_map[domain].append(job)

            if not domain_map:
                lines.append("오늘 새로 발견된 적합한 주니어급 AI 공고가 없습니다. ☕")
            else:
                self._append_jobs_to_lines(lines, domain_map)

        if experienced_jobs:
            lines.append("")
            lines.append("---")
            lines.append("## 📌 [참고] 경력직 AI 공고 (3년 초과)")
            lines.append(f"AI 관련 공고이지만 요구 경력이 높아 주니어 필터링에서 제외된 공고 **{len(experienced_jobs)}건**입니다.")
            lines.append("")
            
            exp_domain_map = {}
            for job in experienced_jobs:
                s_data = job.get('summary_data', {})
                domain = s_data.get('domain', 'Others')
                if domain not in exp_domain_map:
                    exp_domain_map[domain] = []
                exp_domain_map[domain].append(job)
                
            self._append_jobs_to_lines(lines, exp_domain_map, is_experienced=True)

        content = "\n".join(lines)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath

    def _append_jobs_to_lines(self, lines: List[str], domain_map: Dict[str, List[Dict]], is_experienced: bool = False):
        for domain, domain_jobs in sorted(domain_map.items()):
            lines.append(f"### <span class=\"domain-title\">🌐 Domain: {domain}</span>")
            lines.append("")
            
            for job in domain_jobs:
                s_data = job.get('summary_data', {})
                job_title = job.get('position') or job.get('title') or "N/A"
                lines.append(f"#### [{job['company']}]")
                lines.append(f"<div class=\"job-report-item\">")
                lines.append(f"- **채용 직무:** `{job_title}`")
                lines.append("")
                
                # 채용 기간 로직
                start_date = job.get('start_date', '')
                end_date = job.get('end_date', '')
                if "2099" in end_date or "20251231" in end_date or not end_date:
                    period = "상시 채용"
                elif start_date and end_date and start_date != end_date:
                    period = f"{start_date} ~ {end_date}"
                else:
                    period = f"~ {end_date} (마감)"
                
                lines.append(f"- **채용 기간:** `{period}`")
                lines.append(f"- **출처:** `{job.get('source', 'Unknown')}`")
                lines.append(f"- **분류:** `{s_data.get('job_type', 'N/A')}`")
                lines.append(f"- **요구 경력:** `{s_data.get('experience_requirement', 'N/A')}`")
                job_link = job.get('application_url') or job.get('link') or "#"
                lines.append(f"- **링크:** [공고 바로가기]({job_link})")
                lines.append("")
                lines.append("##### 📝 직무 요약")
                lines.append(s_data.get('role_summary') or s_data.get('role', 'N/A'))
                lines.append("")
                lines.append("##### ✅ 필수 요건")
                reqs = s_data.get('key_requirements', [])
                if reqs:
                    for req in reqs:
                        lines.append(f"- {req}")
                else:
                    lines.append("*요건 정보 없음*")
                lines.append("")

                lines.append("##### ⭐ 우대 사항")
                prefs = s_data.get('preferences', [])
                if prefs:
                    for pref in prefs:
                        lines.append(f"- {pref}")
                else:
                    lines.append("*우대 사항 정보 없음*")
                lines.append("")
                lines.append("##### 💡 핵심 요약")
                lines.append(s_data.get('summary', 'N/A'))
                lines.append("")
                lines.append("</div>")
                lines.append("")
                lines.append("---")
                lines.append("")
