from openai import OpenAI


class OpenAIServiceBase:
    def __init__(self, api_key, url, model_name):
        self.api_key = api_key
        self.url = url
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key, base_url=self.url)

    def get_completion(self, prompt):
        messages = [{"role": "user", "content": prompt}]

        response = self.client.chat.completions.create(
            model=self.model_name, messages=messages
        )

        content = response.choices[0].message.content

        return content
