import datetime as dt

import requests
from app_store_scraper import AppStore


def scrape_apps(app_name, how_many):
    app_id = get_app_id(app_name)
    app_ = AppStore(country='id', app_name=app_name, app_id=app_id)

    # Scrape reviews posted since 1 in previous month and limit to 1000 reviews
    current_date = dt.date.today()
    app_.review(how_many=how_many,
                after=dt.datetime(current_date.year, current_date.month - 1, 1),
                # sleep=random.randint(20, 25))
                sleep=None)

    reviews = app_.reviews

    results = []
    for review in reviews:
        rev = review['review']
        print(rev)
        results.append(rev)

    return results


def get_app_id(app_name):
    url = "https://itunes.apple.com/search"
    params = {
        'term': app_name,
        'country': 'id',
        'media': 'software',
        'entity': 'software',
        'limit': 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("Response data from AppStore:")
    print(data)

    if data['resultCount'] > 0:
        app_id = data['results'][0]['trackId']
        return app_id
    else:
        return None
