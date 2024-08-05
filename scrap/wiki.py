import json

import wikipedia


def scrap_wiki(keyword):
    data = []
    jsdata = wiki_search(keyword)
    for cj in range(len(jsdata)):
        item = {"title": jsdata[cj], "abstract": wiki_sum(jsdata[cj])}
        data.append(item)
    print(json.dumps(data))


def wiki_search(keyword, rs=20):
    return wikipedia.search(keyword, results=rs)


def wiki_sum(keyword):
    return wikipedia.summary(keyword, auto_suggest=False)
