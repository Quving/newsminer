from newsboxapi.newsboxapi import NewsboxApi

if __name__ == '__main__':
    newsapi = NewsboxApi()
    articles = newsapi.list_articles()
