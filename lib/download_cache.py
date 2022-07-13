import os
import requests
import json
from datetime import datetime, timedelta
from lib.count_category import create_category_json

FIRST_URL: str = 'https://data.gov.il/api/3/action/datastore_search?resource_id=8c0f314f-583d-48b6-9f5f-4483d95f6848'
BASE_URL: str = 'https://data.gov.il'

def download_questions() -> None:
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
        print("Downloaded: part_" + str(part_count))
        last_question_in_file: int = max(cur["result"]["records"], key=lambda x:x["_id"])["_id"]


def update_if_needed(conf_path: str = "config.json") -> None:
    # if questions_archive is old --> download it
    with open(os.path.join(conf_path), 'r') as config_file:
        conf: dict = json.loads(config_file.read())
    
    # add secret key:
    if conf["last_download_date"] is None:
        conf["secret_key"] = os.urandom(24).hex()

    # checking cache date    
    if (conf["last_download_date"] is None) or ((datetime.now() - datetime.strptime(conf["last_download_date"], r"%m/%d/%Y")).days > 30):
        print("questions cache is old, downloading updated cache")
        download_questions()
        conf["last_download_date"] = datetime.now().strftime(r"%m/%d/%Y") # update time in conf

        # dumping conf dict to config.json file
        with open(conf_path, 'w') as configFile:
            json.dump(conf, configFile)
        
        create_category_json() # initialize categories