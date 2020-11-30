import os
import joblib
import numpy as np

from sklearn import svm

from APIparsers.TheGuardianParser import TheGuardianParser
from MachineLearning.TextManager import ArticleTagsEnum, TextManager


class SvmManager:
    _tags = None
    _adapters = None

    _text_manager = TextManager()
    _parser = TheGuardianParser()

    def __init__(self, *args):
        self._tags = args
        self._adapters = [SvmAdapter(tag) for tag in args]

    def get_train_data(self, articles_count, features_count):
        X = None
        Y = None

        for tag, adapter in zip(self._tags, self._adapters):
            articles = self._parser.get_articles(tag, articles_count)
            new_x, _ = self._text_manager.process_articles(articles, features_count)
            Y = self.add_rows(Y, adapter.get_label_matrix(new_x, len(ArticleTagsEnum)))
            X = self.add_rows(X, new_x)

        return X, Y

    def train_adapters(self, X, Y):
        for tag, adapter in zip(self._tags, self._adapters):
            adapter.train_svm(X, Y[:, tag.value], 100, 0.01)
            print("Adapter {} has been fitting".format(tag))

    def save_all_states(self):
        for adapter in self._adapters:
            adapter.save_svm_state()

    @staticmethod
    def add_rows(matrix, new_matrix):
        return new_matrix if matrix is None else np.vstack([matrix, new_matrix])


class SvmAdapter:
    _svm = None
    _current_tag = ArticleTagsEnum.all

    def __init__(self, tag):
        self._current_tag = tag

    def train_svm(self, x, y, C_coef, sigma_coef):
        self._svm = svm.SVC(C=C_coef, gamma=sigma_coef)
        self._svm.fit(x, y)
        return self._svm

    def get_label_matrix(self, matrix, labels_count):
        label_matrix = np.zeros((len(matrix), labels_count))
        label_matrix[:, self._current_tag.value] = 1
        return label_matrix

    def save_svm_state(self):
        joblib.dump(self._svm, self.get_cache_path(self._current_tag))

    def load_svm_state(self):
        self._svm = joblib.load(self.get_cache_path(self._current_tag))

    @staticmethod
    def get_cache_path(tag):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), "CacheModels", "{}.pkl".format(tag.name))
