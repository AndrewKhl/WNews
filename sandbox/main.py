import warnings

import numpy as np

from wnews.NewsSite.APIparsers.Models import ArticleTagsEnum
from wnews.NewsSite.MachineLearning.SvmLib import SvmManager
from wnews.NewsSite.MachineLearning.TextManager import TextManager


def main():
    warnings.filterwarnings('ignore')
    print(ArticleTagsEnum['sport'])

    text_manager = TextManager()

    articles = text_manager.get_new_articles(ArticleTagsEnum.politics)
    print(len(articles))
    '''


    articles, texts = text_manager.get_articles(ArticleTagsEnum.sport, 10)

    print()
    print(articles[0].title)
    print(articles[0].text)
    print(articles[0].article_link)
    print(articles[0].image_link)
    print(articles[0].last_update)
    '''
    '''
    manager = SvmManager(ArticleTagsEnum.sport, ArticleTagsEnum.economy, ArticleTagsEnum.science,
                         ArticleTagsEnum.musics, ArticleTagsEnum.films, ArticleTagsEnum.politics)

    test_artiles_cnt = 2000
    val_articles_cnt = 100
    dict_len = 1200

    c_arr = np.arange(0.1, 1000, 100)
    #c_arr = [100]
    sigma_arr = [0.0209, 0.0023, 0.0082, 0.0167, 0.0182, 0.0137]#np.arange(0.0001, 0.01, 0.0001) #[0.0209 0.0023 0.0082 0.0167 0.0182 0.0137]

    x, y = manager.get_train_data(test_artiles_cnt, dict_len, save=True)

    manager.train_adapters(x, y, 100, sigma_arr)
    manager.save_all_states()


    x_val, y_val = manager.get_train_data(val_articles_cnt + test_artiles_cnt, dict_len, test_artiles_cnt)

    print("Xval, yval shape", x_val.shape, y_val.shape)

    for c in c_arr:
        for sigma in sigma_arr:
            manager.train_adapters(x, y, c, sigma)
            manager.check_train_adapters(x_val, y_val)
            print("Sigma:", sigma, "Coef:", c)
            print("Best Precision:", manager._precision_vector)
            print("Best C vector:", manager._c_vector)
            print("Best Sigma vector:", manager._sigma_vector)

    for c, sigma in zip(manager._c_vector, manager._sigma_vector):
        manager.train_adapters(x, y, c, sigma)

    #manager.save_all_states()
    '''
    print("Finish")

if __name__ == '__main__':
    main()
