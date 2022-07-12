import json
import os
from flask import Flask, render_template, request, session, make_response
from flask_session import Session

from lib.download_cache import update_if_needed
from lib.get_questions import get_total_questions

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

# Loading questions cache into memory
with open(os.path.join("questions/categories.json"), 'r') as category_file:
        questions: dict = json.loads(category_file.read())

CONFIG_FILE = "config.json"

@app.get("/")
def choose_category():
    # setting default cookie to {"<topic name>": [], ....}
    user_progress: str = request.cookies.get('user_progress', default=str({key: [] for key in questions.keys()})).replace("\'", "\"")
    progress_dict: dict = json.loads(user_progress)
    
    # if a category doesn't exist cookie we add it
    for category in questions.keys():
        progress_dict.setdefault(category, [])

    response = make_response(render_template("index.html", progress_dict=progress_dict, questions = questions))
    response.set_cookie('user_progress', user_progress)
    return response

@app.post("/")
def category_submitted():
    print(request.form)

def main():
    # importing config.json
    with open(os.path.join(CONFIG_FILE), 'r') as config_file:
        conf: dict = json.loads(config_file.read())
    
    # if questions_archive is old --> download it
    update_if_needed(CONFIG_FILE)
    
    # start flask
    app.run(host=conf["flask_host"], port=conf["flask_port"])

if __name__ == "__main__":
    main()
