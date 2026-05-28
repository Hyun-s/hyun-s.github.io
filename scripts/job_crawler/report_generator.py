import os
from datetime import datetime
from typing import List, Dict

class ReportGenerator:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_daily_report(self, jobs: List[Dict]) -> str:
        """
        jobs: List of dicts containing job details and LLM summary data.
        Returns the path of the generated report file.
        """
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
            f"오늘 수집된 공고 중 석사 졸업 및 3년 이하 경력자에게 적합한 공고 **{len(jobs)}건**을 정리했습니다.",
            ""
        ]

        if not jobs:
            lines.append("오늘 새로 발견된 적합한 공고가 없습니다. ☕")
        else:
            # Group by Domain
            domain_map = {}
            for job in jobs:
                domain = job.get('summary_data', {}).get('domain', 'Others')
                if domain not in domain_map:
                    domain_map[domain] = []
                domain_map[domain].append(job)

            for domain, domain_jobs in domain_map.items():
                lines.append(f"## <span class=\"domain-title\">🌐 Domain: {domain}</span>")
                lines.append("")
                
                for job in domain_jobs:
                    s_data = job.get('summary_data', {})
                    job_title = job.get('position') or job.get('title') or "N/A"
                    lines.append(f"### [{job['company']}] {job_title}")
                    lines.append(f"<div class=\"job-report-item\">")
                    lines.append("")
                    lines.append(f"- **출처:** `{job.get('source', 'Unknown')}`")
                    lines.append(f"- **분류:** `{s_data.get('job_type', 'N/A')}`")
                    lines.append(f"- **요구 경력:** `{s_data.get('experience_requirement', 'N/A')}년`")
                    job_link = job.get('application_url') or job.get('link') or "#"
                    lines.append(f"- **링크:** [공고 바로가기]({job_link})")
                    lines.append("")
                    lines.append("#### 📝 직무 요약")
                    lines.append(s_data.get('role_summary') or s_data.get('role', 'N/A'))
                    lines.append("")
                    lines.append("#### ✅ 필수 요건")
                    reqs = s_data.get('key_requirements', [])
                    if reqs:
                        for req in reqs:
                            lines.append(f"- {req}")
                    else:
                        lines.append("*상세 페이지를 분석할 수 없어 필수 요건을 추출하지 못했습니다. 공고 링크를 직접 확인해 주세요.*")
                    lines.append("")

                    lines.append("#### ⭐ 우대 사항")
                    prefs = s_data.get('preferences', [])
                    if prefs:
                        for pref in prefs:
                            lines.append(f"- {pref}")
                    else:
                        lines.append("*상세 페이지 분석 실패로 우대 사항 정보가 없습니다.*")
                    lines.append("")
                    lines.append("#### 💡 핵심 요약")
                    lines.append(s_data.get('summary', 'N/A'))
                    lines.append("")
                    lines.append("</div>")
                    lines.append("")
                    lines.append("---")
                    lines.append("")

        content = "\n".join(lines)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath
