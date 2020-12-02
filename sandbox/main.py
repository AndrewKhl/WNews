import numpy as np
import warnings

from APIparsers.Models import ArticleTagsEnum
from MachineLearning.SvmLib import SvmManager


def main():
    warnings.filterwarnings('ignore')
    manager = SvmManager(ArticleTagsEnum.sport, ArticleTagsEnum.economy, ArticleTagsEnum.science,
                         ArticleTagsEnum.musics, ArticleTagsEnum.films, ArticleTagsEnum.politics)

    test_artiles_cnt = 500
    val_articles_cnt = 100
    dict_len = 1000

    #c_arr = np.arange(0.1, 10000, 100)
    c_arr = [100]
    sigma_arr = np.arange(0.0001, 2, 0.0001)

    x, y = manager.get_train_data(test_artiles_cnt, dict_len)

    print("X, y shapes", x.shape, y.shape)

    x_val, y_val = manager.get_train_data(val_articles_cnt + test_artiles_cnt, dict_len, test_artiles_cnt)

    print("Xval, yval shape", x_val.shape, y_val.shape)

    for c in c_arr:
        for sigma in sigma_arr:
            manager.train_adapters(x, y, c, sigma)
            manager.check_train_adapters(x_val, y_val)
            print("Sigma:", sigma)
            print("Best Precision:", manager._precision_vector)
            print("Best C vector:", manager._c_vector)
            print("Best Sigma vector:", manager._sigma_vector)

    for c, sigma in zip(manager._c_vector, manager._sigma_vector):
        manager.train_adapters(x, y, c, sigma)

    manager.save_all_states()

    print("Finish")


if __name__ == '__main__':
    main()
