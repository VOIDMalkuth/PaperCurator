# Paper Curator

## Targets

*This is only a prototype application for personal usage for now (or maybe forever).*

Filter out paper of interest by LLM Prompt from arxiv on a daily basis, provide additional further analysis like summary, and push to user daily

## Approach

- Get paper from arxiv and store them in a sqlite
- process arxiv paper object by 2 LLMs, first to classify roughly, second to classify carefully and do summarization
- save processed data and do push notification with ServerChan

