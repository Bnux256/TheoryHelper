from bs4 import BeautifulSoup
import random


def parse_html(html: str):
    result = {"options": []}
    soup = BeautifulSoup(html, 'html.parser')

    # getting answer options
    ul_tag = soup.find('ul')
    for li in ul_tag.find_all("li"):
        print(li.text, end=" ")
        result["options"].append((li.text, "correct" in str(li)))
        if "correct" in str(li):
            result["correct"] = li.text
    random.shuffle(result["options"])  # shuffling list

    # getting image
    if len(soup.findAll('img')) > 0:
        result["image"] = soup.findAll('img')[0].get('src')
    else:
        result["image"] = None

    print(result)
    return result
