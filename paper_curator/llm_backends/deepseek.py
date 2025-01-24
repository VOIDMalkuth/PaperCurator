import json

import requests
from llm_backends.utils import IntervalTimer


class DeepSeekService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.timer = IntervalTimer(0.2)
        self.url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_completion(self, prompt, model="deepseek-chat", max_tokens=2048):
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }

        response = requests.post(self.url, headers=self.headers, json=payload)
        response.encoding = "utf-8"

        if response.status_code == 200:
            return json.loads(response.text.split("\n")[0])["choices"][0]["message"][
                "content"
            ]
        else:
            response.raise_for_status()
