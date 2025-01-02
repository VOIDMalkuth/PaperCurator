from fetcher import fetch_new_papers
from processor import process_paper
from publish import do_publish
from storage import DB_PATH, ArxivDB


def collect_and_publish():
    db = ArxivDB(DB_PATH)
    fetch_new_papers(db)
    process_paper(db)
    do_publish(db)


if __name__ == "__main__":
    collect_and_publish()
