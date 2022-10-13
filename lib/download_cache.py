import os
import requests
import json
from datetime import datetime, timedelta
from count_category import create_category_json

FIRST_URL: str = 'https://data.gov.il/api/3/action/datastore_search?resource_id=8c0f314f-583d-48b6-9f5f-4483d95f6848'
BASE_URL: str = 'https://data.gov.il'
CONF_FILE: str = 'config.json'


def download_questions() -> None:
    part_files: list[str] = ['questions/part_0.json'] # keeping a list of paths to file
    if not os.path.exists('questions'):
        os.makedirs('questions')

    # downloading first json file
    first_part = requests.get(FIRST_URL, allow_redirects=True).content
    open(f'questions/part_0.json', 'wb').write(first_part)
    cur: dict = json.loads(first_part)

    question_amount: int = cur["result"]["total"]
    next_part_url: str = BASE_URL + cur["result"]["_links"]["next"]
    last_question_in_file: int = max(cur["result"]["records"],
                                     key=lambda x: x["_id"])["_id"]

    # downloading all the parts until total questions == the last question
    part_count: int = 0
    while (question_amount != last_question_in_file):
        part_count += 1
        filename: str = f'questions/part_{part_count}.json'
        cur_part = requests.get(next_part_url, allow_redirects=True).content
        open(filename, 'wb').write(cur_part)
        cur: dict = json.loads(cur_part)
        next_part_url: str = BASE_URL + cur["result"]["_links"][
            "next"]
        print("Downloaded: part_" + str(part_count))
        last_question_in_file: int = max(cur["result"]["records"],
                                         key=lambda x: x["_id"])["_id"]
        part_files.append(filename)
    return part_files

def add_secret_key(conf_path: str = "config.json") -> None:
    # opening file
    with open(os.path.join(conf_path), 'r') as config_file:
        conf: dict = json.loads(config_file.read())

    # add secret key:
    conf["secret_key"] = os.urandom(24).hex()

    # dumping conf dict to config.json file
    with open(conf_path, 'w') as configFile:
        json.dump(conf, configFile)


def get_total_questions() -> int:
    with open("questions/part_0.json", 'r') as part0:
        part0_dict = json.loads(part0.read())
        return part0_dict["result"]["total"]


def main():
    print('Downloading cache')

    # if file is run standalone, we download cache
    add_secret_key(CONF_FILE)
    temp_files = download_questions() # creates questions cache, returns list of temp files
    create_category_json()  # initialize categories
    print('Download complete!')
    
    # deleting temp paths
    for path in temp_files:
        if os.path.exists(path): 
            os.remove(path)
    print('Temp files deleted')


if __name__ == "__main__":
    main()
