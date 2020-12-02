from enum import Enum


class ArticleTagsEnum(Enum):
    all = 0,
    sport = 1,
    economy = 2,
    science = 3,
    musics = 4,
    films = 5,
    politics = 6


class ArticleModel:
    last_update = None
    text = None
    image_link = None
    article_link = None

    def __init__(self, last_update, text, image_link, article_link):
        self.last_update = last_update
        self.text = text
        self.image_link = image_link
        self.article_link = article_link
