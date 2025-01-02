#!/bin/bash

rm -rf /var/log/app/arxiv.log
touch /var/log/app/arxiv.log

python3 -u /app/paper_curator/scheduler.py