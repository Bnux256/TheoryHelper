import json
import glob


def create_category_json(path: str = "questions/questions.json") -> None:
    """
    for each category we will create a list of the question ids and json file in a dict.
    we will store result in questions/questions.json
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

def decrease_repeat_dict(repeat: dict, category_qustions_ids: dict, category: str):
    """we will go through the repeat dict. if question_id is in category we decrease it.
    returns None or id of question that should be answered now
    """
    return_value = None
    # going through ids
    for key in repeat.keys():
        if int(key) in category_qustions_ids:
            repeat[key] = repeat[key] - 1
            if repeat[key] < 1:
                return_value = int(key)
    
    # if we pop the item
    if return_value is not None:
        repeat.pop(str(key))
    print(repeat)
    return return_value