import re
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
        response = re.sub(r"\s*\n", "\n", response)
        relevant = ("relevant" in response.lower()) and (
            "irrelevant" not in response.lower()
        )
        if relevant:
            res = {"relevance": True}
        else:
            res = {"relevance": False}
        logger.debug(f"Judged paper [{paper_title}]: {res}")
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
        response = re.sub(r"\s*\n", "\n", response)
        resp_list = response.strip().split("\n")
        relevant = ("relevant" in response.lower()) and (
            "irrelevant" not in response.lower()
        )
        if relevant:
            res = {
                "relevance": True,
                "keywords": resp_list[2].strip(),
                "reason": resp_list[0].strip(),
                "summary": "".join(resp_list[3:]),
            }
        else:
            res = {"relevance": False, "reason": resp_list[0]}
        logger.debug(f"Summarized paper [{paper_title}]: {res}")
        return res


def process_paper(db: ArxivDB):
    judge_llm = get_judge_llm_service()
    summarize_llm = get_summarize_llm_service()
    paper_judger = PaperJudger(judge_llm)
    paper_summarizer = PaperSummarizer(summarize_llm)

    total_paper_processed = 0
    total_paper_possible = 0
    total_paper_accepted = 0

    unjudged_paper = db.get_one_paper_by_relevance(-1)
    while unjudged_paper is not None:
        total_paper_processed += 1
        paper_entry_id = unjudged_paper[0]
        paper_title = unjudged_paper[1]
        paper_abstract = unjudged_paper[4]

        paper_judger.llm_service.timer.wait_until_elapsed_interval()
        paper_judger.llm_service.timer.record()
        judge_result = paper_judger.judge_paper(paper_title, paper_abstract)

        relevance = 1 if judge_result["relevance"] else 0
        db.update_paper(paper_entry_id, relevance)

        # check new unsummarized
        unsummarized_paper = db.get_one_paper_by_relevance(1)
        if (
            unsummarized_paper is not None
            and paper_summarizer.llm_service.timer.has_elapsed_interval()
        ):
            total_paper_possible += 1
            paper_entry_id = unsummarized_paper[0]
            paper_title = unsummarized_paper[1]
            paper_abstract = unsummarized_paper[4]

            paper_summarizer.llm_service.timer.record()
            summarize_result = paper_summarizer.summarize_paper(
                paper_title, paper_abstract
            )

            relevance = 100 if summarize_result["relevance"] else 2
            summarize_result["title"] = paper_title
            summarize_result_json = json.dumps(summarize_result)
            db.update_paper(
                paper_entry_id, relevance=relevance, summary=summarize_result_json
            )
            if summarize_result["relevance"]:
                total_paper_accepted += 1

        unjudged_paper = db.get_one_paper_by_relevance(-1)

    unsummarized_paper = db.get_one_paper_by_relevance(1)
    while unsummarized_paper is not None:
        total_paper_possible += 1
        paper_entry_id = unsummarized_paper[0]
        paper_title = unsummarized_paper[1]
        paper_abstract = unsummarized_paper[2]

        paper_summarizer.llm_service.timer.wait_until_elapsed_interval()
        paper_summarizer.llm_service.timer.record()
        summarize_result = paper_summarizer.summarize_paper(paper_title, paper_abstract)

        relevance = 100 if summarize_result["relevance"] else 2
        summarize_result_json = json.dumps(summarize_result)
        db.update_paper(
            paper_entry_id, relevance=relevance, summary=summarize_result_json
        )
        if summarize_result["relevance"]:
            total_paper_accepted += 1

    logger.info(
        f"Total paper processed: {total_paper_processed}, possible: {total_paper_possible}, accepted: {total_paper_accepted}"
    )
