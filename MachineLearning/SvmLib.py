import os
import joblib
import numpy as np

from sklearn import svm

from APIparsers.Models import ArticleTagsEnum
from MachineLearning.TextManager import TextProcessor, TextManager


class SvmManager:
    _tags = None
    _adapters = None
    _c_vector = None
    _sigma_vector = None
    _precision_vector = None

    _text_processor = TextProcessor()
    _text_manager = TextManager()

    def __init__(self, *args):
        self._tags = args
        self._adapters = [SvmAdapter(tag) for tag in args]

        self._c_vector = np.zeros(len(args))
        self._sigma_vector = np.zeros(len(args))
        self._precision_vector = np.zeros(len(args))

    def get_train_data(self, articles_count, features_count, shift_articles=0):
        X = None
        Y = None

        for tag, adapter in zip(self._tags, self._adapters):
            _, texts = self._text_manager.get_articles(tag, articles_count)[shift_articles:]
            new_x, _ = self._text_processor.process_articles(texts, features_count)
            Y = self.add_rows(Y, adapter.get_label_matrix(new_x, len(ArticleTagsEnum)))
            X = self.add_rows(X, new_x)

        return X, Y

    def train_adapters(self, X, Y, C_coef, sigma_coef):
        for tag, adapter in zip(self._tags, self._adapters):
            adapter.train_svm(X, Y[:, tag.value], C_coef, sigma_coef)
            print("Adapter {} has been fitting".format(tag))

    def check_train_adapters(self, Xval, Yval):
        for i, adapter in enumerate(self._adapters):
            current_precision = adapter.check_validation_svm(Xval, Yval[:, self._tags[i].value])
            if self._precision_vector[i] < current_precision:
                self._precision_vector[i] = current_precision
                self._c_vector[i] = adapter.C_coef
                self._sigma_vector[i] = adapter.sigma_coef

    def save_all_states(self):
        for adapter in self._adapters:
            adapter.save_svm_state()

    @staticmethod
    def add_rows(matrix, new_matrix):
        return new_matrix if matrix is None else np.vstack([matrix, new_matrix])


class SvmAdapter:
    _svm = None
    _current_tag = ArticleTagsEnum.all

    C_coef = 0
    sigma_coef = 0

    def __init__(self, tag):
        self._current_tag = tag

    def train_svm(self, x, y, C_coef, sigma_coef):
        self.C_coef = C_coef
        self.sigma_coef = sigma_coef
        self._svm = svm.SVC(C=C_coef, gamma=sigma_coef)
        self._svm.fit(x, y)
        return self._svm

    def check_validation_svm(self, x, y):
        y_predict = self._svm.predict(x)
        good = 0
        for i, predict in enumerate(y_predict):
            if predict == y[i]:
                good += 1
        print("{} SVM Predict: ".format(self._current_tag), good, "Total: ", len(y), "{}%".format(good / len(y) * 100.0))
        return good / len(y) * 100

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
