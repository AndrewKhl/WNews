import requests


class TheGuardianParser:
    _MAX_PAGE_SIZE = 50
    _API_SOURCE = 'http://content.guardianapis.com/search'
    _API_KEY = '5dd8bff4-9d3a-43c5-8526-5743161d4992'

    def __init__(self):
        print('Create The Guardian Pasrser succ')

    def get_articles(self, tag, count_articles):
        page_count = count_articles // self._MAX_PAGE_SIZE + (count_articles % self._MAX_PAGE_SIZE > 0)
        articles = []

        for page_number in range(1, page_count + 1):
            response = self._get_response(tag, page_number)

            if response['status'] == 'ok':
                for item_article in response['results']:
                    articles.append(item_article['fields']['bodyText'])
                    count_articles -= 1
                    if count_articles == 0:
                        break
            else:
                break

        return articles

    def _get_response(self, tag, page):
        return requests.get(
            self._API_SOURCE,
            params={
                "order-by": "newest",
                "show-fields": "bodyText",
                "page-size": self._MAX_PAGE_SIZE,
                "page": page,
                "q": tag.name,
                "api-key": self._API_KEY
            }
        ).json()['response']
