import os
import sys
import json
from bs4 import BeautifulSoup

HERE = os.getcwd()


def get_current_percent():
    filepath = os.path.join(HERE, "coverage_badge.json")

    with open(filepath, "r") as stream:
        body = json.load(stream)

    return int(body["message"].strip("%"))


def get_new_percent():
    filepath = os.path.join(HERE, "htmlcov", "index.html")

    with open(filepath, "r") as f:
        text = f.read()
    soup = BeautifulSoup(text, "html.parser")

    span = soup.find_all("span", attrs={"class": "pc_cov"})[0]

    return int(span.text.strip("%"))


def update_json(percent):
    filepath = os.path.join(HERE, "coverage_badge.json")

    with open(filepath, "r") as stream:
        body = json.load(stream)

    body["message"] = f"{percent}%"

    if percent < 60:
        body["color"] = "red"
    elif (percent >= 60) and (percent < 80):
        body["color"] = "orange"
    else:
        body["color"] = "green"

    with open(filepath, "w") as stream:
        json.dump(body, stream, indent=4, sort_keys=True)


def main():
    current = get_current_percent()
    new = get_new_percent()

    if current == new:
        print("No change in coverage percentage")

    else:
        diff = new - current

        if diff > 0:
            print(f"Coverage has increased by {diff}%")
        else:
            print(f"Coverage has decreased by {diff}%")

        print("Updating coverage badge")
        update_json(new)


if __name__ == "__main__":
    main()
