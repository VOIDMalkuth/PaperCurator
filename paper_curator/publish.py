import datetime
import json
import os
import re

import requests
from loguru import logger
from storage import ArxivDB

SUMMARY_PATH = os.environ.get("SUMMARY_PATH", "paper_summary")


def build_md(judge_res):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    md_doc = f"# Paper Summary {date}\n\n"
    for idx, (paper_entry_id, judgement) in enumerate(judge_res.items()):
        if judgement["relevance"]:
            md_doc += "## " + judgement["title"] + "\n\n"
            md_doc += "Keywords: " + judgement["keywords"] + "\n\n"
            md_doc += "Summary: " + judgement["summary"] + "\n\n"
            md_doc += f"Link: {paper_entry_id}\n\n"
    return md_doc


def sc_send(sendkey, title, desp="", options=None):
    if options is None:
        options = {}
    # 判断 sendkey 是否以 'sctp' 开头，并提取数字构造 URL
    if sendkey.startswith("sctp"):
        match = re.match(r"sctp(\d+)t", sendkey)
        if match:
            num = match.group(1)
            url = f"https://{num}.push.ft07.com/send/{sendkey}.send"
        else:
            raise ValueError("Invalid sendkey format for sctp")
    else:
        url = f"https://sctapi.ftqq.com/{sendkey}.send"
    params = {"title": title, "desp": desp, **options}
    headers = {"Content-Type": "application/json;charset=utf-8"}
    response = requests.post(url, json=params, headers=headers)
    result = response.json()
    return result


def do_publish(db: ArxivDB):
    unpublished_paper = db.get_unpublished_papers()
    paper_dict = {}
    for paper_tuple in unpublished_paper:
        paper_entry_id = paper_tuple[0]
        paper_res = json.loads(paper_tuple[6])
        paper_dict[paper_entry_id] = paper_res
    md_doc = build_md(paper_dict)

    if len(paper_dict) == 0:
        logger.info("No unpublished papers found")
        return

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs(SUMMARY_PATH, exist_ok=True)
    with open(f"{SUMMARY_PATH}/paper_summary_{date}.md", "w") as f:
        f.write(md_doc)

    sc_key = os.environ.get("SC_KEY", "")
    if sc_key == "":
        raise Exception("SC_KEY not set")
    sc_send(
        sc_key,
        f"Paper Summary {date} [{len(paper_dict)}]",
        md_doc,
        {"short": f"Summary of arXiv paper of {date}", "noip": 1},
    )
    logger.info(f"Published {len(paper_dict)} papers")

    for paper_id in paper_dict.keys():
        db.update_paper(paper_id, feed_sent=1)
