import json
import os
import random
from flask import Flask, redirect, render_template, request, session, make_response

from lib.download_cache import update_if_needed
from lib.get_questions import get_total_questions

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Loading questions cache into memory
with open(os.path.join("questions/categories.json"), 'r') as category_file:
    questions: dict = json.loads(category_file.read())

CONFIG_FILE = "config.json"


@app.get("/")
def choose_category():
    # setting default cookie to {"<topic name>": [], ....}
    user_progress: str = request.cookies.get('user_progress',
                                             default=str({
                                                 key: []
                                                 for key in questions.keys()
                                             })).replace("\'", "\"")
    progress_dict: dict = json.loads(user_progress)

    # if a category doesn't exist cookie we add it
    for category in questions.keys():
        progress_dict.setdefault(category, [])

    response = make_response(
        render_template("index.html",
                        progress_dict=progress_dict,
                        questions=questions))
    response.set_cookie('user_progress', user_progress)
    return response


@app.get("/question/")
def category_submitted():
    cur_progress: dict = json.loads(request.cookies.get('user_progress',
                                             default=str({
                                                 key: []
                                                 for key in questions.keys()
                                             })).replace("\'", "\""))
    cur_category: str = request.args.get("category")
    category_qustions_ids = [x["_id"] for x in questions[cur_category]]
    print(category_qustions_ids)
    cur_question_bank = list(
        set(category_qustions_ids) - set(cur_progress[cur_category]))
    random_quesion_id = random.choice(cur_question_bank)
    random_question = list(
        filter(lambda question: question['_id'] == random_quesion_id,
               questions[cur_category]))
    print(random_question)

    response = make_response(render_template("question_viewer.html", cur_category=cur_category, question=random_question))
    cur_progress[cur_category].append(random_quesion_id)
    print(cur_progress)
    response.set_cookie('user_progress', str(cur_progress).replace("\'", "\""))
    return response

def main():
    # importing config.json
    with open(os.path.join(CONFIG_FILE), 'r') as config_file:
        conf: dict = json.loads(config_file.read())

    # create secreat key
    update_if_needed(
        CONFIG_FILE)  # if questions_archive is old --> download it

    app.config['SECRET_KEY'] = conf["secret_key"]

    # start flask
    app.run(host=conf["flask_host"], port=conf["flask_port"])


if __name__ == "__main__":
    main()
