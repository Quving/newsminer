import os
import pickle
import re

from nltk.corpus import stopwords
from progressbar import progressbar

from lda import Lda
from lemmatizer import Lemmatizer
from newsboxapi.newsboxapi import NewsboxApi


def prepare_articles(articles, from_cache=False):
    texts = []
    lemmatizer = Lemmatizer()
    german_stop_words = stopwords.words('german')
    filename = "data/lda-trainingdata.pickle"
    if from_cache:
        with open(filename, 'rb') as file:
            texts = pickle.load(file)
            return texts
    else:
        # Remove '... [+ xxx chars]' pattern from 'content'
        for article in progressbar(articles):
            article_text = ""
            if article.content:
                for text in [article.description, article.content]:
                    text = re.sub('\[.*?\]', '', text)
                    text = " ".join([x for x in text.split() if x.isalnum() or '.' in x])
                    article_text += lemmatizer.lemmatize_text(text=text, verbose=False)

            article_text = [x for x in article_text.split() if x not in german_stop_words]
            texts.append(article_text)

        # Cache lda-trainingdata
        if not os.path.exists("data"):
            os.makedirs("data")
        with open(filename, 'wb') as file:
            pickle.dump(texts, file)

    return texts


if __name__ == '__main__':
    newsapi = NewsboxApi()
    articles = newsapi.list_articles(from_cache=False)
    texts = prepare_articles(articles=articles, from_cache=False)

    # Train LDA
    lda = Lda()
    lda.train_lda(texts=texts, num_topics=20)
    lda.persist_lda()
    lda.visualize()
