import json


def get_total_questions() -> int:
    with open("questions/part_0.json", 'r') as part0:
        part0_dict = json.loads(part0.read())
        return part0_dict["result"]["total"]
