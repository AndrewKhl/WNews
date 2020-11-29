import json
import requests

from APIparsers.the_guardian_parser import ArticleTagsEnum, TheGuardianParser


def main():
    api_key = "5dd8bff4-9d3a-43c5-8526-5743161d4992"
    #req = "https://content.guardianapis.com/search?q=\"mitochondrial%20donation\"&tag=politics/politics&from-date=2014-01-01&api-key=test"
    #req = "https://content.guardianapis.com/tags&api-key=5dd8bff4-9d3a-43c5-8526-5743161d4992"
    req = "http://content.guardianapis.com/search?order-by=newest&show-fields=bodyText&page-size=50&q=politics&api-key={}"

    guardian_parser = TheGuardianParser()
    articles = guardian_parser.get_articles(ArticleTagsEnum.all, 5)

    #articles = response['response']['results']

    #print(response)
    print("Articles count =", len(articles))
    #print(articles)
    #for row in articles:
        #print(row)
     #   print(row['fields']['bodyText'])

    print("Finish")


if __name__ == '__main__':
    main()
