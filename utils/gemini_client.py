'''import requests
import json

class GeminiClient:
    def __init__(self, api_key):
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"

    def summarize(self, text):
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Summarize the following project tasks:\n{text}"}
                    ]
                }
            ]
        }

        response = requests.post(
            self.url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]

'''

import os
import requests
import json


class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set in environment variables")

        # Free-tier, stable model
        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/gemini-flash-lite-latest:generateContent"
            f"?key={self.api_key}"
        )

    def summarize(self, text: str) -> str:
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": (
                                "You are a project management assistant.\n"
                                "Summarize the following project tasks clearly:\n\n"
                                f"{text}"
                            )
                        }
                    ]
                }
            ]
        }

        response = requests.post(
            self.url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=30
        )

        # Raise error if request failed
        response.raise_for_status()

        result = response.json()

        return result["candidates"][0]["content"]["parts"][0]["text"]
