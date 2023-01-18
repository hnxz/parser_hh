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
    return count_tag


def top_tags():
    top_tag_lst =[]
    for i,v in count_tags().items():
        top_tag_lst.append((v,i))

    result = {}
    top_10tags = (sorted(top_tag_lst, reverse=True)[:11])
    for d in top_10tags:
        result[d[1]] = d[0]
    with open('top_tags.txt', 'w') as file:
        for key, value in result.items():
            file.write(f'{key} => {value}\n')




from_json_to_list()
handler_lst()
count_tags()
top_tags()