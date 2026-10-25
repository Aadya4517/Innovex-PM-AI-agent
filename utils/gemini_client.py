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


class GeminiClient:
    """Small REST client for Gemini; the API key is never sent to the browser."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            "models/gemini-flash-lite-latest:generateContent"
        )

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        response = requests.post(
            self.url,
            headers={"Content-Type": "application/json", "x-goog-api-key": self.api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=25,
        )
        response.raise_for_status()
        payload = response.json()
        candidates = payload.get("candidates", [])
        if not candidates:
            raise RuntimeError("Gemini returned no response candidates")
        parts = candidates[0].get("content", {}).get("parts", [])
        answer = "\n".join(part.get("text", "") for part in parts).strip()
        if not answer:
            raise RuntimeError("Gemini returned an empty response")
        return answer

    def summarize(self, tasks: list[dict]) -> str:
        task_data = "\n".join(
            f"- {task.get('id')}: {task.get('title')} | status={task.get('status')} | "
            f"due={task.get('due_date') or 'not set'} | priority={task.get('priority', 'unknown')}"
            for task in tasks
        ) or "No tasks are currently available."
        return self.generate(
            "You are a project manager assistant. Summarize this project data in concise "
            "plain language. Mention progress, urgent deadlines, delayed or blocked work, "
            "and next actions. Do not invent dependencies or facts.\n\n"
            f"Tasks:\n{task_data}"
        )

    def answer(self, query: str, tasks: list[dict]) -> str:
        task_data = "\n".join(
            f"- {task.get('id')}: {task.get('title')} | status={task.get('status')} | "
            f"due={task.get('due_date') or 'not set'} | priority={task.get('priority', 'unknown')}"
            for task in tasks
        ) or "No tasks are currently available."
        return self.generate(
            "Answer the project manager's question using only the task data below. "
            "If the data does not contain the answer, say so. Be concise.\n\n"
            f"Question: {query}\n\nTasks:\n{task_data}"
        )
