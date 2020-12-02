from enum import Enum
from datetime import datetime


class ArticleTagsEnum(Enum):
    all = 0,
    sport = 1,
    economy = 2,
    science = 3,
    musics = 4,
    films = 5,
    politics = 6


class ArticleModel:
    _SHORT_TEXT_LENGTH = 200
    _DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    last_update_obj = None
    last_update = None
    title = None
    full_text = None
    text = None
    image_link = None
    article_link = None

    def __init__(self, title, last_update, text, image_link, article_link):
        self.title = title
        self.full_text = text
        self.image_link = image_link
        self.article_link = article_link

        self.text = text[: self._SHORT_TEXT_LENGTH] + '...'
        self.last_update_obj = datetime.strptime(last_update, self._DATETIME_FORMAT)
        self.last_update = self.last_update_obj.strftime("%d/%m/%Y %H:%M")