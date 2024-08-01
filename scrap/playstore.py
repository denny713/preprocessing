from google_play_scraper import search, reviews, Sort

def scrape_play(app_name):
    count = 200
    rvws, _ = reviews(
        get_app_id(app_name),
        lang='id',
        country='id',
        sort=Sort.NEWEST,
        count=count
    )

    print(rvws)
    results = []

    for rvw in rvws:
        rev = rvw['content']
        print(rev)
        results.append(rev)

    return results


def get_app_id(app_name):
    results = search(app_name, lang='en', country='us')
    print(results)

    if results:
        app_id = results[0]['appId']
        return app_id
    else:
        return None
