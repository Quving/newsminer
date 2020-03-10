import re

from newsboxapi.newsboxapi import NewsboxApi

if __name__ == '__main__':
    # Get articles from endpoint
    newsapi = NewsboxApi()
    articles = newsapi.list_articles()

    # Remove '... [+ xxx chars]' pattern from 'content'
    for article in articles:
        article.content = re.sub('... \[.*?\]', '', article.content)
        print(article.content.split("."))
