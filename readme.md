# **TheoryHelper**
## Easily learn for the Israeli driving theory exam for private cars.
### Built using Python + Flask + Bootstrap
### Doesn't use javascript!
### Try it now: [bnux256.github.io/TheoryHelper/](https://bnux256.github.io/TheoryHelper/)
---

![demo image](/docs/images/demo.png)
## Disclaimer
I created this site to help me prepare for the test and published it to help others. The code is open source and the site has no warranty.

## What does it do?
Uses the official question repository and picks random questions from the chosen category. Uses spaced repetition (simpler variation on the [Leitner system](https://en.wikipedia.org/wiki/Leitner_system)) to maximize the learning efficiency.

---
## Deployment Guide - 
### Using AWS Lambda functions - 
Before you begin, make sure you are running Python 3.7/3.8/3.9 (or higher if supported by the Lambda runtime) and you have a valid AWS account and your [AWS credentials file](https://blogs.aws.amazon.com/security/post/Tx3D6U6WSFGOK2H/A-New-and-Standardized-Way-to-Manage-Credentials-in-the-AWS-SDKs) is properly installed.

On Linux:
create a venv - `python3 -m venv env`
enter venv - `source env/bin/activate`
install packages - `pip3 install -r requirements-lambda.txt`
create cache - `python3 lib/download_cache.py`
deploy - `zappa deploy`

### Using Docker + Docker Compose - 
- git clone - `git clone https://github.com/Bnux256/TheoryHelper.git`
- build Docker image - `docker build . bnux256/theoryhelper`
- run service: docker compose up -d \
TheoryHelper should now be running on [localhost:8000](localhost:8000)!
---

## Directory Structure - 
```
.
├── config.json
├── docker-compose.yml
├── Dockerfile
├── docs
│   └── images
│       └── demo.png
├── frontend
│   ├── iframe.html
│   ├── index.html
│   └── question_viewer.html
├── lib
│   ├── count_category.py
│   ├── download_cache.py
│   ├── html_parser.py
│   └─── __init__.py
├── main.py
├── questions
│   └── questions.json
├── readme.md
├── requirements-lambda.txt
├── requirements.txt
└── zappa_settings.json
```