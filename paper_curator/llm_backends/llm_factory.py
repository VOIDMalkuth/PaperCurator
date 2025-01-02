import os

from llm_backends.deepseek import DeepSeekService
from llm_backends.poe import PoeService
from llm_backends.qc import QCService

LLM_CHOICES_MAP = {
    "POE": PoeService,
    "QC": QCService,
    "DEEPSEEK": DeepSeekService,
}

LLM_API_KEY_POSTFIX = "_API_KEY"

JUDGE_LLM_CHOICE_KEY = "JUDGE_LLM"
SUMMARIZE_LLM_CHOICE_KEY = "SUMMARIZE_LLM"

LLM_SERVICE_MAP = {}


def get_llm_service(key: str):
    llm_service = LLM_SERVICE_MAP.get(key, None)
    if llm_service is None:
        api_key = os.environ.get(key + LLM_API_KEY_POSTFIX, "")
        if api_key.strip() == "":
            raise Exception(f"API key for {key} is not set")
        llm_service = LLM_CHOICES_MAP[key](api_key)
        LLM_SERVICE_MAP[key] = llm_service
    return llm_service


def get_judge_llm_service():
    llm_type = os.environ.get(JUDGE_LLM_CHOICE_KEY, "DEEPSEEK")
    return get_llm_service(llm_type)


def get_summarize_llm_service():
    llm_type = os.environ.get(SUMMARIZE_LLM_CHOICE_KEY, "DEEPSEEK")
    return get_llm_service(llm_type)
