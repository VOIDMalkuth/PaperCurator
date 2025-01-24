from llm_backends.utils import IntervalTimer
from llm_backends.openai_service_base import OpenAIServiceBase


class DeepSeekChatService(OpenAIServiceBase):
    API_URL = "https://api.deepseek.com/"
    MODEL_NAME = "deepseek-chat"

    def __init__(self, api_key, interval=0.25):
        super().__init__(
            api_key, DeepSeekChatService.API_URL, DeepSeekChatService.MODEL_NAME
        )
        self.timer = IntervalTimer(interval)


class DeepSeekReasonerService(OpenAIServiceBase):
    API_URL = "https://api.deepseek.com/"
    MODEL_NAME = "deepseek-reasoner"

    def __init__(self, api_key, interval=1.5):
        super().__init__(
            api_key, DeepSeekReasonerService.API_URL, DeepSeekReasonerService.MODEL_NAME
        )
        self.timer = IntervalTimer(interval)
