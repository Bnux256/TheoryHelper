import json
import os
import random
from flask import Flask, redirect, render_template, request, session, make_response, url_for

from lib.html_parser import parse_html
from lib.download_cache import update_if_needed
from lib.count_category import decrease_repeat_dict

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Loading questions cache into memory
with open(os.path.join("questions/questions.json"), 'r') as category_file:
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
def send_question():
    """after we recived a category, we send either a random question in that topic that hasn't been aswered yet or a question that the user struggled with before."""
    cur_progress: dict = json.loads(
        request.cookies.get('user_progress',
                            default=str({
                                key: []
                                for key in questions.keys()
                            })).replace("\'", "\""))  # getting user's progress
    try:
        cur_category: str = request.args.get("category")  # getting category
        category_qustions_ids = [
            x["_id"] for x in questions[cur_category]
        ]  # making a list of all question id's in the current category
        repeat_cookie: dict = json.loads(
            request.cookies.get('repeat', default=str({}).replace("\'", "\"")))
        repeat_question_id = decrease_repeat_dict(repeat_cookie,
                                                  category_qustions_ids,
                                                  cur_category)

        if repeat_question_id is None:
            # if no question need to be repeated right now
            cur_question_bank = list(
                set(category_qustions_ids) - set(cur_progress[cur_category])
            )  # we aren't intrested in the intersection between the sets - only questions that weren't answered
            random_quesion_id = random.choice(cur_question_bank)
            cur_progress[cur_category].append(random_quesion_id)

        else:
            # if question needs to be answered now
            random_quesion_id = repeat_question_id

        random_question = list(
            filter(lambda question: question['_id'] == random_quesion_id,
                   questions[cur_category])
        )[0]  # searching in the list of dicts for the question object
        response = make_response(
            render_template("question_viewer.html",
                            question=random_question,
                            parsed_question=parse_html(
                                random_question["description4"])))
        response.set_cookie('user_progress',
                            str(cur_progress).replace("\'", "\""))
        response.set_cookie('repeat', str(repeat_cookie).replace("\'", "\""))
        return response

    except KeyError:
        return redirect(url_for("choose_category"))


@app.get("/iscorrect/")
def is_ans_correct():
    if request.args.get("option") == "True":
        # answer is true
        emoji: str = "tick"
        message: str = "כל הכבוד!"
        response = make_response(
            render_template("iframe.html", emoji=emoji, message=message))
    else:
        # answer is wrong
        emoji: str = "X"
        message: str = "לא נכון. התשובה הנכונה היא: " + request.args.get(
            "correct_answer")
        response = make_response(
            render_template("iframe.html", emoji=emoji, message=message))

        # creating a cookie with "<id>": 4 - the 3 means: in 4 turns ask the user this question again
        repeat_cookie: dict = json.loads(
            request.cookies.get('repeat', default=str({}).replace("\'", "\"")))
        repeat_cookie[request.args.get("question_id")] = 4
        response.set_cookie('repeat', str(repeat_cookie).replace("\'", "\""))
    return response


def main():
    print('aaaaa')
    # importing config.json
    with open(os.path.join(CONFIG_FILE), 'r') as config_file:
        conf: dict = json.loads(config_file.read())

    update_if_needed(
        CONFIG_FILE)  # if questions_archive is old --> download it

    app.config['SECRET_KEY'] = conf["secret_key"]

    # start flask
    app.run(host=conf["flask_host"], port=conf["flask_port"])


if __name__ == "__main__":
    main()