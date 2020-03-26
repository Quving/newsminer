import datetime
import os
import pickle
import re

from nltk.corpus import stopwords
from progressbar import progressbar

from lda import Lda
from lemmatizer import Lemmatizer
from minioapi.minioapi import MinioApi
from newsboxapi.newsboxapi import NewsboxApi

NUM_TOPIC = 5
PUBLISHED_BEFORE_N_DAYS = 7
LANGUAGE = 'de'


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
    # Settings
    use_cache = False
    update_html = True

    # Retrieve and prepare dataset
    newsapi = NewsboxApi()
    publishedAfter = (datetime.date.today() - datetime.timedelta(days=PUBLISHED_BEFORE_N_DAYS)).isoformat()
    articles = newsapi.list_articles(language=LANGUAGE, publishedAfter=publishedAfter, from_cache=use_cache)
    texts = prepare_articles(articles=articles, from_cache=use_cache)

    # Train LDA
    lda = Lda()
    lda.train_lda(texts=texts, num_topics=NUM_TOPIC)
    lda.persist_lda()
    lda.export_html()
    # lda.visualize()

    # Update lda html for newsmap
    if update_html:
        minioapi = MinioApi()
        bucket_name = 'newsmap'
        minioapi.create_bucket(bucket_name=bucket_name)
        minioapi.upload_file(bucket_name=bucket_name, filename='index.html', file='artifacts/lda/index.html')
        minioapi.make_public(bucket_name=bucket_name)
