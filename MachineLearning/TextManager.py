import re
import nltk
import collections
import numpy as np
from nltk.stem import PorterStemmer
from enum import Enum


class ArticleTagsEnum(Enum):
    all = 0,
    sport = 1,
    economy = 2,
    science = 3,
    musics = 4,
    films = 5,
    politics = 6


class TextManager:
    _html_regs = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    _url_regs = re.compile(
        'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
    _email_regs = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    _number_regs = re.compile('[0-9.]+')
    _text_regs = re.compile('[#&%+:;\[\]/|><=`()@,\'\"!?\-}{*_\-®•“’”…‘–]')
    _porter_stemmer = PorterStemmer()

    current_counter = collections.Counter()

    def __init__(self):
        #nltk.download('punkt')
        pass

    def process_articles(self, articles):
        self.current_counter.clear()
        matrix = [self._convert_article(article) for article in articles]

        current_dict = [t[0] for t in self.current_counter.most_common(100)]
        return np.array([self._get_features_vector(row, current_dict) for row in matrix]), current_dict

    @staticmethod
    def _get_features_vector(words, dictionary):
        vector = np.zeros(len(dictionary))
        for i, key in enumerate(dictionary):
            if key in words:
                vector[i] = 1
        return vector

    def _convert_article(self, article):
        article = re.sub(self._html_regs, '', article.lower())
        article = re.sub(self._url_regs, 'httpaddr', article)
        article = re.sub(self._email_regs, 'emailaddr', article)
        article = re.sub(self._number_regs, ' number ', article)
        article = article.replace('$', 'dollar ')
        article = re.sub(self._text_regs, '', article)

        words = nltk.word_tokenize(article)

        for i, word in enumerate(words):
            words[i] = self._porter_stemmer.stem(word)
            self.current_counter[words[i]] += 1

        return words