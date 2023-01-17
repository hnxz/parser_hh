import json
from collections import Counter


def from_json_to_list():
    with open('vacansy.json') as file:
        data = json.load(file)
    return data


def handler_lst():
    tags_lst = []
    for item in from_json_to_list():
        for key, value in item.items():
            if key == 'tags':
                tags_lst.extend(value)
    return tags_lst


def count_tags():
    count_tag = Counter(handler_lst())
    print(count_tag) # нужно отсортировать по значению


from_json_to_list()
handler_lst()
count_tags()