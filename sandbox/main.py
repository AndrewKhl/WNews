from APIparsers.TheGuardianParser import TheGuardianParser
from MachineLearning.TextManager import ArticleTagsEnum, TextManager
from MachineLearning.SvmLib import SvmAdapter, SvmManager


def main():
    manager = SvmManager(ArticleTagsEnum.sport, ArticleTagsEnum.films)

    x, y = manager.get_train_data(100, 100)
    manager.train_adapters(x, y)
    manager.save_all_states()

    print("Finish")


if __name__ == '__main__':
    main()
