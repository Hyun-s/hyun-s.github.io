import os
from datetime import datetime
from typing import List, Dict

class ReportGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_daily_report(self, jobs: List[Dict], experienced_jobs: List[Dict] = None) -> str:
        if experienced_jobs is None:
            experienced_jobs = []
            
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M")
        file_time_str = now.strftime("%H%M")
        
        main_filename = f"{today_str}-{file_time_str}.md"
        main_filepath = os.path.join(self.output_dir, main_filename)
        
        extra_filename = f"{today_str}-{file_time_str}-experienced.md"
        extra_filepath = os.path.join(self.output_dir, extra_filename)

        # 1. Main Report
        main_lines = self._build_frontmatter(f"Daily AI Job Report: {today_str} {time_str}", now)
        main_lines.append(f"# 📅 AI Job Daily Report ({today_str} {time_str})")
        main_lines.append("")
        
        filtered_exp_jobs = self._filter_ai_jobs(experienced_jobs)
        if filtered_exp_jobs:
            link_path = extra_filename.replace('.md', '')
            main_lines.append(f"> 💡 **[경력직 AI 공고 (3년 초과) {len(filtered_exp_jobs)}건 별도 페이지에서 확인하기 🚀](../{link_path}/)**")
            main_lines.append("")

        main_lines.append(f"오늘 수집된 공고 중 석사 졸업 및 3년 이하 경력자에게 적합한 주니어급 AI 공고 **{len(jobs)}건**을 정리했습니다.")
        main_lines.append("")

        if not jobs:
            main_lines.append("오늘 새로 발견된 적합한 주니어급 AI 공고가 없습니다. ☕")
        else:
            self._build_job_sections(main_lines, jobs, today_str)

        with open(main_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(main_lines))

        # 2. Extra Report (Experienced)
        if filtered_exp_jobs:
            extra_lines = self._build_frontmatter(f"Experienced AI Job Report: {today_str} {time_str}", now)
            extra_lines.append(f"# 👔 경력직 AI Job Report ({today_str} {time_str})")
            extra_lines.append("")
            extra_lines.append(f"> 💡 **[👉 주니어급 AI 공고 리포트로 돌아가기](../{main_filename.replace('.md', '')}/)**")
            extra_lines.append("")
            extra_lines.append(f"AI 관련 공고이지만 요구 경력이 높아(3년 초과) 주니어 필터링에서 제외된 공고 **{len(filtered_exp_jobs)}건**입니다.")
            extra_lines.append("")
            self._build_job_sections(extra_lines, filtered_exp_jobs, today_str)

            with open(extra_filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(extra_lines))
                
        return main_filepath

    def _filter_ai_jobs(self, jobs: List[Dict]) -> List[Dict]:
        filtered = []
        for job in jobs:
            domain = job.get('summary_data', {}).get('domain', 'Others')
            if domain.lower() not in ['others', 'none-ai', 'none']:
                filtered.append(job)
        return filtered

    def _build_frontmatter(self, title, date_obj):
        return [
            "---",
            f"title: \"{title}\"",
            f"date: {date_obj.isoformat()}",
            f"tags: [\"Job Report\", \"AI\", \"Research\"]",
            "categories: [\"Career\"]",
            "---",
            ""
        ]

    def _build_job_sections(self, lines: List[str], jobs: List[Dict], today_str: str):
        # Group by Active vs Closing Today
        active_jobs = []
        closing_jobs = []
        
        for job in jobs:
            end_date = job.get('end_date', '')
            if end_date == today_str:
                closing_jobs.append(job)
            else:
                active_jobs.append(job)
                
        if active_jobs:
            lines.append("## 🟢 신규 및 진행중인 공고")
            lines.append("")
            self._append_domain_groups(lines, active_jobs, today_str)
            
        if closing_jobs:
            lines.append("## 🔴 오늘 마감되는 공고")
            lines.append("")
            self._append_domain_groups(lines, closing_jobs, today_str)

    def _append_domain_groups(self, lines: List[str], jobs: List[Dict], today_str: str):
        domain_map = {}
        for job in jobs:
            domain = job.get('summary_data', {}).get('domain', 'Others')
            if domain not in domain_map:
                domain_map[domain] = []
            domain_map[domain].append(job)
            
        for domain, domain_jobs in sorted(domain_map.items()):
            lines.append(f"### <span class=\"domain-title\">🌐 Domain: {domain}</span>")
            lines.append("")
            
            for job in domain_jobs:
                s_data = job.get('summary_data', {})
                job_title = job.get('position') or job.get('title') or "N/A"
                
                start_date = job.get('start_date', '')
                end_date = job.get('end_date', '')
                if not end_date or "2099" in end_date or "20251231" in end_date:
                    period = "상시 채용"
                elif start_date and start_date != end_date:
                    period = f"{start_date} ~ {end_date}"
                else:
                    period = f"마감일: {end_date}"

                lines.append(f"#### [{job['company']}]")
                lines.append(f"<div class=\"job-report-item\">")
                lines.append("")
                
                # Using HTML tags to force proper rendering of the list
                lines.append("<ul>")
                lines.append(f"<li><strong>채용 직무:</strong> <code>{job_title}</code></li>")
                lines.append(f"<li><strong>채용 기간:</strong> <code>{period}</code></li>")
                lines.append(f"<li><strong>출처:</strong> <code>{job.get('source', 'Unknown')}</code></li>")
                lines.append(f"<li><strong>분류:</strong> <code>{s_data.get('job_type', 'N/A')}</code></li>")
                lines.append(f"<li><strong>요구 경력:</strong> <code>{s_data.get('experience_requirement', 'N/A')}</code></li>")
                
                job_link = job.get('application_url') or job.get('link') or "#"
                lines.append(f"<li><strong>링크:</strong> <a href=\"{job_link}\" target=\"_blank\">공고 바로가기</a></li>")
                lines.append("</ul>")
                
                lines.append("")
                lines.append("<h3>📝 직무 요약</h3>")
                lines.append(f"<p>{s_data.get('role_summary') or s_data.get('role', 'N/A')}</p>")
                lines.append("")
                
                lines.append("<h3>✅ 필수 요건</h3>")
                reqs = s_data.get('key_requirements', [])
                if reqs:
                    lines.append("<ul>")
                    for req in reqs:
                        lines.append(f"<li>{req}</li>")
                    lines.append("</ul>")
                else:
                    lines.append("<p><em>요건 정보 없음</em></p>")
                lines.append("")

                lines.append("<h3>⭐ 우대 사항</h3>")
                prefs = s_data.get('preferences', [])
                if prefs:
                    lines.append("<ul>")
                    for pref in prefs:
                        lines.append(f"<li>{pref}</li>")
                    lines.append("</ul>")
                else:
                    lines.append("<p><em>우대 사항 정보 없음</em></p>")
                lines.append("")
                
                lines.append("<h3>💡 핵심 요약</h3>")
                lines.append(f"<p>{s_data.get('summary', 'N/A')}</p>")
                lines.append("")
                lines.append("</div>")
                lines.append("")
                lines.append("---")
                lines.append("")
