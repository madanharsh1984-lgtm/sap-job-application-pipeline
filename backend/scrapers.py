import requests
import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

class ApifyScraper:
    def __init__(self):
        # Commercial model: uses a central master API token
        self.api_token = os.getenv("APIFY_TOKEN")
        self.actor_id = "harvestapi/linkedin-post-search"

    def scrape_linkedin_posts(self, keywords: List[str]) -> List[Dict]:
        if not self.api_token:
            print("APIFY_TOKEN not set")
            return []

        # Construct the API call to Apify actor
        # https://apify.com/harvestapi/linkedin-post-search
        # Input uses searchQueries
        payload = {
            "searchQueries": keywords,
            "maxPosts": 50,
            "proxyConfig": {"useApifyProxy": True}
        }

        url = f"https://api.apify.com/v2/acts/{self.actor_id}/run-sync-get-dataset-items?token={self.api_token}"
        
        try:
            response = requests.post(url, json=payload, timeout=300)
            if response.status_code == 201 or response.status_code == 200:
                return response.json()
            else:
                print(f"Apify Error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            print(f"Scraper Exception: {str(e)}")
            return []

    def extract_lead_data(self, raw_post: Dict) -> Dict:
        """Extract lead fields for our database."""
        # This matches the schema and internal extraction logic
        content = raw_post.get("content", "")
        # Basic extraction logic similar to prototype
        import re
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
        
        return {
            "platform": "LinkedIn",
            "job_title": raw_post.get("jobTitle", "Job Position"),
            "company": raw_post.get("companyName", "Recruiter Post"),
            "location": raw_post.get("location", "Not specified"),
            "raw_text": content,
            "recruiter_email": emails[0] if emails else None
        }
