import requests
from datetime import datetime, timedelta
from BaseFeeder import BaseFeeder
from NewsModels.RawNews import RawNews


class TheNYTimesFeeder(BaseFeeder):
    _API_SOURCE = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    _API_KEY = 'nQnmGmGuvIhGcnLChoLoKRVRuCuB3buG'
    _SOURCE_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def request_to_source(self):
        return requests.get(
            self._API_SOURCE,
            params={
                "api-key": self._API_KEY,
                "source": "The New York Times",
                # "from-date": (datetime.utcnow() - timedelta(seconds=self._update_time)).strftime(self._SOURCE_DATETIME_FORMAT),
                "sort": "newest",
                "fq": "The New York Times",
                "page": 1,
            }
        ).json()

    def get_news_items(self, response):
        return response['response']['docs'] if 'docs' in response['response'] else None

    def convert_to_raw_news(self, source_response):
        news = []
        for item in source_response:
            n = RawNews(source="TheNewYorkTimes",
                        title=item['headline']['main'],
                        link=item['web_url'],
                        text=f'{item["snippet"]} {item["lead_paragraph"]}',
                        time=item['pub_date'])
            news.append(n)
        return news


timesFeeder = TheNYTimesFeeder(update_time=10)
timesFeeder.start()
