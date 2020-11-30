from APIparsers.TheGuardianParser import TheGuardianParser
from MachineLearning.TextManager import ArticleTagsEnum, TextManager


def main():
    guardian_parser = TheGuardianParser()
    articles = guardian_parser.get_articles(ArticleTagsEnum.films, 10)

    print("Articles count =", len(articles))

    text_manager = TextManager()

    matrix, dict = text_manager.process_articles(articles)

    print(matrix)
    print(dict)

    print("Finish")


if __name__ == '__main__':
    main()
