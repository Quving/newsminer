import os
import pickle
import sys

import requests

from config import Config, Logger
from newsboxapi.models import Article


class NewsboxApi:
    AUTH_TOKEN = Config.auth_token
    API_ENDPOINT = Config.api_endpoint

    logger = Logger.logger

    def list_articles(self,
                      language='',
                      published_after='',
                      publishedAt='',
                      publishedBefore='',
                      from_cache=False):
        """
        Returns a list of all articles that is stored in the configured api endpoint. The returned list contains
         instances of the class 'Article'.
        """
        filename = "cache/articles.pickle"
        if from_cache:
            self.logger.info("Use cached newsarticles of {}.".format(Config.api_endpoint))

            with open(filename, 'rb') as file:
                articles = pickle.load(file)
                return articles
        else:
            self.logger.info("Fetch all news-articles from {}.".format(Config.api_endpoint))
            headers = {
                'Authorization': 'Bearer {}'.format(self.AUTH_TOKEN),
            }
            params = ()

            # Parse params
            if language:
                params += (('language', language),)

            if published_after:
                params += (('publishedAfter', published_after),)

            if publishedAt:
                params += (('publishedAt', publishedAt),)

            if publishedBefore:
                params += (('publishedBefore', publishedBefore),)

            url = '{}/news/articles/'.format(self.API_ENDPOINT)  # Initial url for page 1

            list_of_articles = []
            while url:
                response = requests.get(url=url, headers=headers, params=params)
                if response.status_code == 200:
                    response = response.json()
                    url = response['next']  # Overrite url to retrieve next pages.

                    articles = response['results']
                    for json in articles:
                        articles = Article(json=json)
                        list_of_articles.append(articles)
                elif response.status_code == 401:
                    self.logger.error("NEWSMINER_AUTH_TOKEN expired.")
                    sys.exit(1)
                else:
                    self.logger.error(
                        "Unknown error occured while fetching neww articles from {}".format(Config.api_endpoint))
                    sys.exit(1)
            if not os.path.exists("cache"):
                os.makedirs("cache")
            with open(filename, 'wb') as file:
                pickle.dump(list_of_articles, file)
        return list_of_articles
