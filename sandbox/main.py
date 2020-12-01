from MachineLearning.TextManager import ArticleTagsEnum
from MachineLearning.SvmLib import SvmManager


def main():
    manager = SvmManager(ArticleTagsEnum.sport, ArticleTagsEnum.films)

    test_artiles_cnt = 1000
    val_articles_cnt = 1000
    dict_len = 1000


    x, y = manager.get_train_data(test_artiles_cnt, dict_len)
    manager.train_adapters(x, y)

    x_val, y_val = manager.get_train_data(val_articles_cnt + test_artiles_cnt, dict_len, test_artiles_cnt)

    manager.check_train_adapters(x_val, y_val)

    #manager.save_all_states()

    print("Finish")


if __name__ == '__main__':
    main()
