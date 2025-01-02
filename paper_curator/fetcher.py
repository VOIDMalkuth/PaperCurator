import datetime

import arxiv
from loguru import logger
from storage import ArxivDB

categories = [
    "cs.AI",  # Artificial Intelligence
    "cs.CL",  # Computation and Language
    "cs.CV",  # CV
    "cs.DC",  # Distributed, Parallel, and Cluster Computing
    "cs.AR",  # Hardware Architecture
    "cs.LG",  # Machine Learning
    "cs.MA",  # Multiagent Systems
    "cs.PF",  # Performance
]

DEFAULT_PAGE_SIZE = 500
DEFAULT_MAX_RESULTS = 3000


def get_entry_id_part(entry_id):
    part = entry_id.split("/")[-1]
    part_without_reversion = part.split("v")[0]
    part_tuple = tuple(map(lambda x: int(x), part_without_reversion.split(".")))
    return part_tuple


def fetch_new_from_arxiv_by_entry_id(start_from_entry_id: str):
    start_from = get_entry_id_part(start_from_entry_id)
    client = arxiv.Client(page_size=DEFAULT_PAGE_SIZE, delay_seconds=5.0)
    cat_exp_list = ["cat:" + category for category in categories]
    query_exp = " OR ".join(cat_exp_list)
    search = arxiv.Search(
        query=query_exp,
        max_results=DEFAULT_MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    results_full_iter = client.results(search)
    paper_list = []
    max_entry_id = start_from
    for result in results_full_iter:
        paper_entry_id_tuple = get_entry_id_part(result.entry_id)
        if paper_entry_id_tuple > start_from:
            paper_list.append(result)
            max_entry_id = max(max_entry_id, paper_entry_id_tuple)
        else:
            break
    return paper_list, max_entry_id


def fetch_new_from_arxiv_by_date(days_to_now: int):
    today = datetime.datetime.now(tz=datetime.timezone.utc)
    client = arxiv.Client(page_size=DEFAULT_PAGE_SIZE, delay_seconds=5.0)
    cat_exp_list = ["cat:" + category for category in categories]
    query_exp = " OR ".join(cat_exp_list)
    search = arxiv.Search(
        query=query_exp,
        max_results=DEFAULT_MAX_RESULTS,
        sort_by=arxiv.SortCriterion.SubmittedDate,
    )
    results_full_iter = client.results(search)
    paper_list = []
    max_entry_id = (-1, -1)
    for result in results_full_iter:
        paper_entry_id_tuple = get_entry_id_part(result.entry_id)
        if today - result.published <= datetime.timedelta(days=days_to_now):
            paper_list.append(result)
            max_entry_id = max(max_entry_id, paper_entry_id_tuple)
        else:
            break
    return paper_list, max_entry_id


def fetch_new_papers(db: ArxivDB, last_paper_id=None):
    if last_paper_id is None:
        last_paper_id = db.get_data_info("last_paper_id")

    logger.info(f"Fetching new papers from ArXiv, last paper id: {last_paper_id}")
    if last_paper_id is None:
        paper_list, max_entry_id = fetch_new_from_arxiv_by_date(3)
    else:
        paper_list, max_entry_id = fetch_new_from_arxiv_by_entry_id(last_paper_id)

    logger.info(f"Fetched {len(paper_list)} new papers from ArXiv")
    if max_entry_id == (-1, -1):
        return

    db.update_data_info("last_paper_id", ".".join(map(str, max_entry_id)))
    total_new_papers_inserted = 0
    for paper in paper_list:
        success = db.add_paper_if_not_exists(
            paper.entry_id, paper.title, paper.entry_id, paper.published, paper.summary
        )
        if success:
            total_new_papers_inserted += 1
    logger.info(f"Inserted {total_new_papers_inserted} new papers to database")

    return len(paper_list)
