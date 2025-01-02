import json

from llm_backends.llm_factory import get_judge_llm_service, get_summarize_llm_service
from loguru import logger
from prompts import CLASSIFY_AND_SUMMARIZE_PROMPT, CLASSIFY_PROMPT
from storage import ArxivDB


class PaperJudger:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.prompt_template = CLASSIFY_PROMPT

    def judge_paper(self, paper_title, paper_abstract):
        question = self.prompt_template.format(
            title=paper_title, abstract=paper_abstract.replace("\n", " ")
        )
        response = self.llm_service.get_completion(question)
        resp_list = response.strip().split("\n")
        if resp_list[0].strip().lower() == "relevant":
            res = {"relevance": True}
        else:
            res = {"relevance": False}
        logger.debug(f"Judged paper {paper_title}: {res}")
        return res


class PaperSummarizer:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.prompt_template = CLASSIFY_AND_SUMMARIZE_PROMPT

    def summarize_paper(self, paper_title, paper_abstract):
        question = self.prompt_template.format(
            title=paper_title, abstract=paper_abstract.replace("\n", " ")
        )
        response = self.llm_service.get_completion(question)
        resp_list = response.strip().split("\n")
        if resp_list[0].strip().lower() == "relevant":
            res = {
                "relevance": True,
                "keywords": resp_list[1].strip(),
                "summary": "".join(resp_list[2:]),
            }
        else:
            res = {"relevance": False, "reason": "".join(resp_list[1:])}
        logger.debug(f"Summarized paper {paper_title}: {res}")
        return res


def process_paper(db: ArxivDB):
    judge_llm = get_judge_llm_service()
    summarize_llm = get_summarize_llm_service()
    paper_judger = PaperJudger(judge_llm)
    paper_summarizer = PaperSummarizer(summarize_llm)

    unjudged_paper = db.get_one_paper_by_relevance(-1)
    while unjudged_paper is not None:
        paper_entry_id = unjudged_paper[0]
        paper_title = unjudged_paper[1]
        paper_abstract = unjudged_paper[4]

        paper_judger.llm_service.timer.wait_until_elapsed_interval()
        judge_result = paper_judger.judge_paper(paper_title, paper_abstract)
        relevance = 1 if judge_result["relevance"] else 0
        db.update_paper(paper_entry_id, relevance)

        # check new unsummarized
        unsummarized_paper = db.get_one_paper_by_relevance(1)
        if (
            unsummarized_paper is not None
            and paper_summarizer.llm_service.timer.has_elapsed_interval()
        ):
            paper_entry_id = unsummarized_paper[0]
            paper_title = unsummarized_paper[1]
            paper_abstract = unsummarized_paper[4]
            summarize_result = paper_summarizer.summarize_paper(
                paper_title, paper_abstract
            )
            relevance = 100 if summarize_result["relevance"] else 2
            summarize_result["title"] = paper_title
            summarize_result_json = json.dumps(summarize_result)
            db.update_paper(
                paper_entry_id, relevance=relevance, summary=summarize_result_json
            )

        unjudged_paper = db.get_one_paper_by_relevance(-1)

    unsummarized_paper = db.get_one_paper_by_relevance(1)
    while unsummarized_paper is not None:
        paper_entry_id = unsummarized_paper[0]
        paper_title = unsummarized_paper[1]
        paper_abstract = unsummarized_paper[2]
        summarize_result = paper_summarizer.summarize_paper(paper_title, paper_abstract)
        logger.debug(f"Summarized paper {paper_entry_id}: {summarize_result}")
        relevance = 100 if summarize_result["relevance"] else 2
        summarize_result_json = json.dumps(summarize_result)
        db.update_paper(
            paper_entry_id, relevance=relevance, summary=summarize_result_json
        )
