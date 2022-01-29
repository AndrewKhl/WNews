import time
from abc import ABCMeta, abstractmethod
from kafka import KafkaProducer


class BaseFeeder:
    __metaclass__ = ABCMeta

    def __init__(self, update_time=60):
        self._update_time = update_time
        self._producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                       value_serializer=lambda x: x.toJSON().encode('utf-8'))

    @abstractmethod
    def get_new_articles(self):
        "Получить новости из источника"

    @abstractmethod
    def convert_to_raw_news(self, source_response):
        "Перевод полученных данных в NewRaw модель"

    def start(self):
        while True:
            source_response = self.get_new_articles()
            if source_response['status'] == 'ok':
                if 'results' in source_response:
                    items = source_response['results']
                    if len(items) > 0:
                        news = self.convert_to_raw_news(items)
                        print(news)
                        for ne in news:
                            self._producer.send("RawNewsCollection", value=ne)
            time.sleep(self._update_time)

