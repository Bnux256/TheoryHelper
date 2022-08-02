# **TheoryHelper**
## Easily learn for the Israeli driving theory exam for private cars.
### Built using Python + Flask + Bootstrap
### Try it now: [theoryhelper.bnux256.duckdns.org](https://theoryhelper.bnux256.duckdns.org)
---

![demo image](/docs/images/demo.png)
## What does it do?

 Uses the offical question repository and picks random questions from the chosen category. Uses spaced repetition (simpler variation on the [Leitner system](https://en.wikipedia.org/wiki/Leitner_system)) to maximize the learning efficiency.

---
## Deployment Guide - 
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
│   └── images
│       └── demo.png
├── frontend
│   ├── static
│   │   └── assets
│   │       ├── dist
│   │       │   ├── css
│   │       │   │   ├── bootstrap.rtl.min.css
│   │       │   │   └── bootstrap.rtl.min.css.map
│   │       │   └── js
│   │       │       └── bootstrap.bundle.min.js.map
│   │       └── logo.png
│   └── templates
│       ├── iframe.html
│       ├── index.html
│       └── question_viewer.html
├── lib
│   ├── count_category.py
│   ├── download_cache.py
│   ├── html_parser.py
│   └── __init__.py
├── main.py
├── README.md
└── requirments.txt
```
---
