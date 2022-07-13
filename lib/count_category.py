import json
import glob


def create_category_json(path: str = "questions/categories.json") -> None:
    """
    for each category we will create a list of the question ids and json file in a dict.
    we will store result in questions/categories.json
    """
    categories: dict = {}
    question_part_count: int = len(glob.glob1('questions', "part*"))

    # go through the question parts
    cur_par_index: int = 0
    for part in range(question_part_count):
        with open(f"questions/part_{cur_par_index}.json", 'r') as part_file:
            cur_part = json.loads(part_file.read())["result"]["records"]
            for question in cur_part:
                if question["category"] not in categories.keys():
                    categories[question["category"]] = [question]
                else:
                    categories[question["category"]].append(question)

        cur_par_index += 1

    # dumping dict in file
    with open(path, 'w') as categoriesFile:
        json.dump(categories, categoriesFile, ensure_ascii=False)


def category_counter(questions: dict) -> dict:
    """given a dict {a:[1,2,3], b:[2,3]} will return: {a:3, b:2}"""
