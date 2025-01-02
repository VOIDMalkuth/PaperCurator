import json

import requests
from llm_backends.utils import IntervalTimer


class QCService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.timer = IntervalTimer(3)
        self.url = "https://maas.qc-ai.cn/api/v1/qc-maas/chat/completions/apikey"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def get_completion(self, prompt, model="Qwen2-7B-Instruct(NV)", max_tokens=1024):
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
