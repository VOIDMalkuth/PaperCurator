import os
import sys
import time

import schedule
from collect_and_publish import collect_and_publish
from loguru import logger

# Remove default logger
logger.remove()
# Add console logger
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
)
# Add file logger
logger.add(
    "/var/log/app/arxiv.log",
    rotation="10 MB",  # Rotate when file reaches 10MB
    retention="1 week",  # Keep logs for 1 week
    compression="zip",  # Compress rotated logs
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
)


def run_script():
    try:
        collect_and_publish()
    except Exception as e:
        logger.error(f"Error running collect_paper_and_publish: {e}")


def main():
    daily_run_time = os.environ.get("DAILY_RUN_TIME", "05:30")
    tz = os.environ.get("TZ", "Asia/Shanghai")
    schedule.every().day.at(daily_run_time, tz).do(run_script)

    logger.info(
        f"Scheduler started, scheduled to run at {daily_run_time} everday at {tz} time."
    )

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    main()
