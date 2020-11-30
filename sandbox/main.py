from APIparsers.TheGuardianParser import TheGuardianParser
from MachineLearning.TextManager import ArticleTagsEnum, TextManager
from MachineLearning.SvmManager import SvmManager

def main():
    guardian_parser = TheGuardianParser()

    current_tag = ArticleTagsEnum.films

    articles = guardian_parser.get_articles(current_tag, 10)

    print("Articles count =", len(articles))

    text_manager = TextManager()

    matrix, dict = text_manager.process_articles(articles, 100)

    svm = SvmManager(current_tag)

    yy = svm.get_label_matrix(matrix, len(ArticleTagsEnum))

    for x, y in zip(matrix, yy):
        print(x, y)

    print("Finish")


if __name__ == '__main__':
    main()
