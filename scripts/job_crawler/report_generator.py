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
        today_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{today_str}.md"
        filepath = os.path.join(self.output_dir, filename)

        # Hugo Frontmatter
        lines = [
            "---",
            f"title: \"Daily AI Job Report: {today_str}\"",
            f"date: {datetime.now().isoformat()}",
            f"tags: [\"Job Report\", \"AI\", \"Research\"]",
            "categories: [\"Career\"]",
            "---",
            "",
            f"# 📅 AI Job Daily Report ({today_str})",
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
                lines.append(f"## 🌐 Domain: {domain}")
                lines.append("")
                
                for job in domain_jobs:
                    s_data = job.get('summary_data', {})
                    lines.append(f"### [{job['company']}] {job['title']}")
                    lines.append(f"- **분류:** `{s_data.get('job_type', 'N/A')}`")
                    lines.append(f"- **요구 경력:** `{s_data.get('experience_requirement', 'N/A')}년`")
                    lines.append(f"- **링크:** [공고 바로가기]({job['link']})")
                    lines.append("")
                    lines.append("#### 📝 직무 요약")
                    lines.append(s_data.get('role_summary', 'N/A'))
                    lines.append("")
                    lines.append("#### ✅ 필수 요건")
                    for req in s_data.get('key_requirements', []):
                        lines.append(f"- {req}")
                    lines.append("")
                    lines.append("#### ⭐ 우대 사항")
                    for pref in s_data.get('preferences', []):
                        lines.append(f"- {pref}")
                    lines.append("")
                    lines.append("#### 💡 핵심 요약")
                    lines.append(s_data.get('summary', 'N/A'))
                    lines.append("")
                    lines.append("---")
                    lines.append("")

        content = "\n".join(lines)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath
