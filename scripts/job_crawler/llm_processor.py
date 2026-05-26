import os
import json
import logging
from google import genai
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class LLMProcessor:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-1.5-flash"

    def summarize_job(self, job_title: str, company: str, description: str) -> Optional[Dict]:
        prompt = f"""
        다음은 '{company}'의 '{job_title}' 채용 공고 내용입니다.
        내용을 분석하여 다음 항목을 포함한 JSON 형식으로 요약해주세요:
        
        1. role: 직군/역할 요약 (한 문장)
        2. deadline: 마감일 (YYYY-MM-DD 형식, 명시되지 않았거나 '상시'인 경우 null)
        3. preferences: 주요 우대사항 (최대 5개 리스트)
        4. summary: 공고 핵심 요약 (2-3문장)

        공고 내용:
        {description}

        반드시 JSON 형식으로만 답변하세요. 다른 설명은 제외하세요.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            
            text = response.text
            # Clean up JSON if necessary
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            return json.loads(text)
        except Exception as e:
            logger.error(f"Error processing LLM for {job_title} at {company}: {e}")
            return None

if __name__ == "__main__":
    # Test with a dummy description
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        processor = LLMProcessor(api_key)
        result = processor.summarize_job("AI Research Engineer", "Test Company", "우리는 확산 모델 전문가를 찾습니다. PyTorch 숙련자 우대. 마감일은 2026년 12월 31일입니다.")
        print(json.dumps(result, indent=2, ensure_ascii=False))
