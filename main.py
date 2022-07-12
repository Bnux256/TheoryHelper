import requests
import os
import json
from flask import Flask

FIRST_URL: str = 'https://data.gov.il/api/3/action/datastore_search?resource_id=8c0f314f-583d-48b6-9f5f-4483d95f6848'
BASE_URL: str = 'https://data.gov.il'

app = Flask(__name__)

def download_questions():
    if not os.path.exists('questions'):
        os.makedirs('questions')

    # downloading first json file
    first_part = requests.get(FIRST_URL, allow_redirects=True).content
    open(f'questions/part_0.json', 'wb').write(first_part)
    cur: dict = json.loads(first_part)

    question_amount: int = cur["result"]["total"]
    next_part_url: str = 'https://data.gov.il' + cur["result"]["_links"]["next"]
    last_question_in_file: int = max(cur["result"]["records"], key=lambda x:x["_id"])["_id"]

    # downloading all the parts until total questions == the last question
    part_count: int = 0
    while(question_amount != last_question_in_file):
        part_count+=1
        cur_part = requests.get(next_part_url, allow_redirects=True).content
        open(f'questions/part_{part_count}.json', 'wb').write(cur_part)
        cur: dict = json.loads(cur_part)
        next_part_url: str = 'https://data.gov.il' + cur["result"]["_links"]["next"]
        print("Downloaded: part_" + part_count)
        last_question_in_file: int = max(cur["result"]["records"], key=lambda x:x["_id"])["_id"]

def main():
    download_questions()
if __name__ == "__main__":
    main()