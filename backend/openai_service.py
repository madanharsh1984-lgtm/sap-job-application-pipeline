import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("AI_MODEL", "gpt-4-turbo-preview")

    def analyze_and_tailor(self, resume_text: str, job_description: str):
        if not self.api_key:
            return "AI Service not configured. Please add OPENAI_API_KEY to .env"

        prompt = f"""
        You are an expert Career Coach and ATS Optimizer.
        
        TASK:
        1. Analyze the provided Master Resume and the Job Description (JD).
        2. Rewrite the Professional Summary to align perfectly with the JD.
        3. Identify the top 5 key achievements from the resume that most directly prove the candidate can do the job described in the JD.
        4. Suggest 3 specific keywords or skills to add to the 'Skills' section.

        MASTER RESUME:
        {resume_text}

        JOB DESCRIPTION:
        {job_description}

        OUTPUT FORMAT (JSON):
        {{
            "new_summary": "...",
            "highlighted_achievements": ["...", "...", "..."],
            "new_skills": ["...", "...", "..."],
            "match_score": 85
        }}
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional resume writer."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"AI Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Exception in AI Service: {str(e)}"
