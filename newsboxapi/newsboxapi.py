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

    def list_articles(self, from_cache=False):
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
            self.logger.info("Fetch all newsarticles from {}.".format(Config.api_endpoint))
            headers = {
                'Authorization': 'Bearer {}'.format(self.AUTH_TOKEN),
            }

            url = '{}/news/articles/'.format(self.API_ENDPOINT)  # Initial url for page 1

            list_of_articles = []
            while url:
                response = requests.get(url=url, headers=headers)
                if response.status_code == 200:
                    response = response.json()
                    url = response['next']  # Overrite url to retrieve next pages.

                    articles = response['results']
                    for json in articles:
                        articles = Article(json=json)
                        list_of_articles.append(articles)
                elif response.status_code == 401:
                    self.logger.error("NEWSMINER_AUTH_TOKEN expired.")
                    sys.exit("Script aborted due to error.")
                else:
                    self.logger.error(
                        "Unknown error occured while fetching neww articles from {}".format(Config.api_endpoint))
                    sys.exit("Unknown server error.")
            if not os.path.exists("cache"):
                os.makedirs("cache")
            with open(filename, 'wb') as file:
                pickle.dump(list_of_articles, file)
        return list_of_articles
