import os
import json
import logging
import requests
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class LLMProcessor:
    def __init__(self, api_key: str = "empty", base_url: str = "http://localhost:8000/v1"):
        self.base_url = base_url
        self.model_name = "local-coder" # From your docker-compose config
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def summarize_job(self, job_title: str, company: str, description: str) -> Optional[Dict]:
        prompt = f"""
        당신은 AI/ML 전문 리크루팅 어드바이저입니다. 다음 채용 공고를 정밀 분석하여 '신입~석사급 주니어(경력 3년 이하) AI 연구원/엔지니어'에게 적합한지 판단해야 합니다.

        공고 내용:
        회사: {company}
        포지션: {job_title}
        본문:
        {description}

        [판단 및 요약 규칙]
        1. domain: 기술 도메인 (예: "Vision", "LLM", "Diffusion", "Audio", "NLP", "Multi-modal", "General AI")
           - 만약 AI/ML과 직접적인 관련이 없는 일반적인 개발 직군(Front-end, Back-end, DevOps, App Dev 등)이라면 "None-AI"로 분류하세요.
        2. job_type: 구체적 직무 성격 (예: "모델 경량화(Compression)", "모델 개발", "Agent 개발", "Research")
        3. is_suitable: 다음 조건을 **모두** 만족해야 true입니다. 하나라도 어긋나면 false입니다.
           - **AI/ML 전문성:** 모델 개발, 연구, 최적화 등 AI 핵심 로직을 다루는 직무여야 함. (단순히 AI 서비스를 호출하는 일반 개발직무는 false)
           - **경력 제한:** 요구 경력이 '신입'이거나 '1~3년' 사이여야 함. '5년 이상', '시니어급' 키워드가 있거나 필수 경력이 4년을 초과하면 false.
           - **석사 우대:** 석사 졸업생이 지원하기에 적절한 수준이어야 함.
        4. experience_requirement: 요구되는 최소 경력 연수 (숫자만, 신입은 0, 명시되지 않으면 0으로 가정)
        5. key_requirements: 필수 자격 요건 (리스트)
        6. preferences: 주요 우대사항 (리스트)
        7. summary: 공고 핵심 요약 (2-3문장)

        반드시 아래 JSON 형식으로만 답변하세요:
        {{
          "domain": "...",
          "job_type": "...",
          "is_suitable": true/false,
          "experience_requirement": 0,
          "role_summary": "...",
          "key_requirements": ["..."],
          "preferences": ["..."],
          "summary": "..."
        }}
        """

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        try:
            logger.info(f"Attempting summarization with local LLM ({self.model_name})")
            response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            text = result['choices'][0]['message']['content']
            
            # Clean up JSON if necessary
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(text)
            logger.info(f"Successfully summarized using local LLM")
            return data
        except Exception as e:
            logger.error(f"Failed with local LLM: {e}")
            return None
