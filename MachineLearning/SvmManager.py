import joblib
import numpy as np

from sklearn import svm
from MachineLearning.TextManager import ArticleTagsEnum


class SvmManager:
    _svm = None
    _current_tag = ArticleTagsEnum.all
    _model_cache_path = "/CacheModels/{}.pkl".format(_current_tag)

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
        joblib.dump(self._svm, self._model_cache_path)

    def load_svm_state(self):
        self._svm = joblib.load(self._model_cache_path)


