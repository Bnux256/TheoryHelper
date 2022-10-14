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
### Using Docker + Docker Compose - 
- git clone - `git clone https://github.com/Bnux256/TheoryHelper.git`
- build Docker image - `docker build . bnux256/theoryhelper`
- run service: docker compose up -d \
TheoryHelper should now be running on [localhost:8000](localhost:8000)!
---