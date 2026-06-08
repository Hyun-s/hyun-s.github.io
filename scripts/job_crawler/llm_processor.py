import os
import json
import logging
import requests
import base64
from typing import Dict, Optional, List
from io import BytesIO
try:
    from PIL import Image
except ImportError:
    Image = None

logger = logging.getLogger(__name__)

class LLMProcessor:
    def __init__(self, api_key: str = "empty", base_url: str = "http://localhost:8000/v1"):
        self.base_url = base_url
        self.model_name = "local-coder" # From your docker-compose config
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def _get_image_data(self, image_url: str) -> Optional[str]:
        """Download image, resize if needed, and return as base64 string"""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            if Image:
                try:
                    img = Image.open(BytesIO(response.content))
                    # Check if image is too large
                    max_width = 1024
                    max_height = 2048
                    
                    if img.width > max_width or img.height > max_height:
                        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                        
                    # Convert back to bytes
                    buffer = BytesIO()
                    # Convert to RGB to save as JPEG (prevent transparency issues)
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    img.save(buffer, format="JPEG", quality=85)
                    img_bytes = buffer.getvalue()
                except Exception as img_e:
                    logger.warning(f"PIL Image processing failed, using original bytes: {img_e}")
                    img_bytes = response.content
            else:
                img_bytes = response.content
                
            return base64.b64encode(img_bytes).decode('utf-8')
        except Exception as e:
            logger.error(f"Failed to download image {image_url}: {e}")
            return None

    def classify_job(self, job_data: dict, categories: list, image_urls: List[str] = None) -> Optional[dict]:
        """
        Use LLM to classify job posting into categories and extract structured data
        """
        description = job_data.get('description', '')
        has_images = image_urls and len(image_urls) > 0
        
        if (not description or len(description) < 50) and not has_images:
            logger.warning(f"No content for classification: {job_data.get('title')}")
            return {
                "primary_category": "others",
                "subcategories": [],
                "skills": [],
                "confidence": 1.0,
                "reasoning": "공고 본문 및 이미지가 없어 분류가 불가능합니다."
            }

        category_names = [c['slug'] for c in categories]
        category_names.append("others")

        prompt = f"""
        Analyze this job posting (text and/or images) and classify it into the most appropriate category.
        If it is NOT an AI/ML related job (e.g., general development, sales, HR, non-tech), classify it as 'others'.

        Company: {job_data.get('company')}
        Position: {job_data.get('title')}
        Text Description: {description[:2000]}

        Available Categories:
        {json.dumps(category_names, indent=2, ensure_ascii=False)}

        Return JSON with:
        - primary_category: slug of best matching category
        - subcategories: array of relevant subcategory slugs
        - skills: array of extracted skills
        - confidence: 0.0-1.0 confidence score
        - reasoning: brief explanation in Korean
        """

        content = [{"type": "text", "text": prompt}]
        
        if has_images:
            # Only send first 3 images to avoid context limits
            for img_url in image_urls[:3]:
                # If local VLM can access external URLs, we could send the URL.
                # But base64 is safer for local APIs.
                base64_img = self._get_image_data(img_url)
                if base64_img:
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
                    })

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a job classification assistant that can see images."},
                {"role": "user", "content": content}
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }

        try:
            logger.info(f"Attempting classification with local VLM ({self.model_name})")
            response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload, timeout=180)
            if not response.ok:
                logger.error(f"VLM API Error {response.status_code}: {response.text}")
            response.raise_for_status()
            
            result = response.json()
            text = result['choices'][0]['message']['content']
            
            # Clean up JSON
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            return json.loads(text)
        except Exception as e:
            logger.error(f"Failed classification with local VLM: {e}")
            return None

    def summarize_job(self, job_title: str, company: str, description: str, image_urls: List[str] = None) -> Optional[Dict]:
        has_images = image_urls and len(image_urls) > 0
        prompt = f"""
        당신은 AI/ML 전문 리크루팅 어드바이저입니다. 제공된 텍스트와 이미지를 정밀 분석하여 '신입~석사급 주니어(경력 3년 이하) AI 연구원/엔지니어'에게 적합한지 판단하세요.

        공고 내용:
        회사: {company}
        포지션: {job_title}
        본문: {description[:1000]}

        [판단 및 요약 규칙]
        1. domain: 기술 도메인 (예: "Vision", "LLM", "Diffusion", "Audio", "NLP", "Multi-modal", "General AI", "Agentic AI", "Applied AI")
        2. job_type: 구체적 직무 성격
        3. is_suitable: AI 핵심 로직(모델, 에이전트 개발/연구/최적화)을 다루고, 요구 경력이 신입~3년 사이면 true.
        4. experience_requirement: 공고에 명시된 요구 경력 (예: "신입", "경력 3년 이상", "경력 무관" 등 텍스트 그대로 기재)
        5. role_summary: 주요 업무 구체적 기술
        6. key_requirements: 필수 자격 요건 (리스트). 텍스트나 이미지에 명시된 내용을 빠짐없이 정확하게 추출하세요.
        7. preferences: 주요 우대사항 (리스트). 텍스트나 이미지에 적혀있는 우대사항 문구를 생략하지 말고 있는 그대로 추출하세요.
        8. summary: 공고 핵심 요약 (2-3문장)

        반드시 아래 JSON 형식으로만 답변하세요:
        {{
          "domain": "...",
          "job_type": "...",
          "is_suitable": true/false,
          "experience_requirement": "...",
          "role_summary": "...",
          "key_requirements": ["..."],
          "preferences": ["..."],
          "summary": "..."
        }}
        """

        content = [{"type": "text", "text": prompt}]
        if has_images:
            for img_url in image_urls[:3]:
                base64_img = self._get_image_data(img_url)
                if base64_img:
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}
                    })

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": content}
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        try:
            logger.info(f"Attempting summarization with local VLM ({self.model_name})")
            response = requests.post(f"{self.base_url}/chat/completions", headers=self.headers, json=payload, timeout=180)
            if not response.ok:
                logger.error(f"VLM API Error {response.status_code}: {response.text}")
            response.raise_for_status()
            
            result = response.json()
            text = result['choices'][0]['message']['content']
            
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            return json.loads(text)
        except Exception as e:
            logger.error(f"Failed with local VLM: {e}")
            return None
