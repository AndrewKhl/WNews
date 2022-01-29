import requests
from datetime import datetime, timedelta
from BaseFeeder import BaseFeeder
from NewsModels.RawNews import RawNews


class TheGuardianFeeder(BaseFeeder):
    _API_SOURCE = 'http://content.guardianapis.com/search'
    _API_KEY = '5dd8bff4-9d3a-43c5-8526-5743161d4992'
    _SOURCE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def get_new_articles(self):
        return requests.get(
            self._API_SOURCE,
            params={
                "api-key": self._API_KEY,
                # "from-date": (datetime.utcnow() - timedelta(seconds=self._update_time)).strftime(self._SOURCE_DATETIME_FORMAT),
                "order-by": "newest",
                "show-fields": "bodyText",
                "page-size": 5,
                "page": 1,
            }
        ).json()['response']

    def convert_to_raw_news(self, source_response):
        news = []
        for item in source_response:
            n = RawNews(source="TheGuardian",
                        title=item['webTitle'],
                        link=item['webUrl'],
                        text=item['fields']['bodyText'],
                        time=item['webPublicationDate'])
            news.append(n)
        return news


guardianFeeder = TheGuardianFeeder(update_time=10)
guardianFeeder.start()
