import os
import json
import logging
import google.generativeai as genai
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class LLMProcessor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Try different model identifiers to avoid 404
        self.model_names = ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro"]

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

        for model_name in self.model_names:
            try:
                logger.info(f"Attempting summarization with model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                
                text = response.text
                # Clean up JSON if necessary
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                
                # Basic validation that it's JSON
                data = json.loads(text)
                logger.info(f"Successfully summarized using {model_name}")
                return data
            except Exception as e:
                logger.error(f"Failed with model {model_name}: {e}")
                continue
        
        logger.error("All LLM models failed to process the job description.")
        return None
