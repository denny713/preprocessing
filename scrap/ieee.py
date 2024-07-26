import requests
import urllib.parse
import json


def scrape_ieee(keyword):
    max_paper = 200
    url = 'http://ieeexploreapi.ieee.org/api/v1/search/articles?max_records=' + str(max_paper)
    api_key = '6hu2a2ms42qzx8thtvz52mzk'
    return result_process(query_run(url, api_key, keyword, max_paper), max_paper)


def query_run(url, key, search, max_paper):
    query_url = url + '&querytext=(' + urllib.parse.quote(search) + ')' + '&apikey=' + key
    print("URL: " + query_url)

    response = requests.get(query_url)
    print("Response: " + response.text)

    output = open(search + "_raw.txt", "w", encoding="utf-8")
    output.write(response.text)
    output.close()

    return result_process(response.text, max_paper)


def result_process(data, max_paper):
    jsn = json.loads(data)

    count = 0
    unique_terms = {}

    for article in jsn['articles']:
        count += 1

        print("-----------------------------------------------------------")
        print(article['title'])
        print("-----------------------------------------------------------")

        # Extracts IEEE Terms from the JSON
        if 'ieee_terms' in article['index_terms']:
            ieee_terms = article['index_terms']['ieee_terms']['terms']
            print("IEEE Terms Found:", len(ieee_terms))

            for term in ieee_terms:
                if term in unique_terms:
                    unique_terms[term] += 1
                else:
                    unique_terms[term] = 1

        # Extracts Author Terms from the JSON
        if 'author_terms' in article['index_terms']:
            author_terms = article['index_terms']['author_terms']['terms']
            print("Author Terms Found:", len(author_terms))

            for term in author_terms:
                if term in unique_terms:
                    unique_terms[term] += 1
                else:
                    unique_terms[term] = 1

        print()

    print("Processing Complete.  Processed", count, "papers")

    if jsn['total_records'] > max_paper:
        print("WARNING:", jsn['total_records'], "records found. Modify your query to get a narrower search")

    return unique_terms