import numpy as np
import warnings

from MachineLearning.TextManager import ArticleTagsEnum
from MachineLearning.SvmLib import SvmManager


def main():
    warnings.filterwarnings('ignore')
    manager = SvmManager(ArticleTagsEnum.sport, ArticleTagsEnum.films)

    test_artiles_cnt = 100
    val_articles_cnt = 10
    dict_len = 100

    #c_arr = np.arange(0.1, 1000, 100)
    c_arr = [100]
    sigma_arr = np.arange(0.001, 0.01, 0.001)

    x, y = manager.get_train_data(test_artiles_cnt, dict_len)

    print("X, y shapes", x.shape, y.shape)

    x_val, y_val = manager.get_train_data(val_articles_cnt + test_artiles_cnt, dict_len, test_artiles_cnt)

    print("Xval, yval shape", x_val.shape, y_val.shape)

    for c in c_arr:
        for sigma in sigma_arr:
            manager.train_adapters(x, y, c, sigma)
            manager.check_train_adapters(x_val, y_val)

    #manager.save_all_states()

    print("Precision:", manager._precision_vector)
    print("C vector:", manager._c_vector)
    print("Sigma vector:", manager._sigma_vector)
    print("Finish")


if __name__ == '__main__':
    main()
