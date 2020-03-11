import pickle
import re

from nltk.corpus import stopwords
from progressbar import progressbar

from lda import Lda
from lemmatizer import Lemmatizer
from newsboxapi.newsboxapi import NewsboxApi

if __name__ == '__main__':

    # Get articles from endpoint
    newsapi = NewsboxApi()
    articles = newsapi.list_articles(from_cache=True)

    lemmatizer = Lemmatizer()
    german_stop_words = stopwords.words('german')
    texts = []

    # Remove '... [+ xxx chars]' pattern from 'content'
    for article in progressbar(articles):
        article_text = ""
        if article.content:
            for text in [article.description, article.content]:
                text = re.sub('\[.*?\]', '', text)
                text = " ".join([x for x in text.split() if x.isalnum() or '.' in x])
                article_text += lemmatizer.lemmatize_text(text=text)

        article_text = [x for x in article_text.split() if x not in german_stop_words]
        texts.append(article_text)

    # Cache lda-trainingdata
    with open('data/lda-trainingdata.pickle', 'wb') as file:
        pickle.dump(texts, file)

    with open('data/lda-trainingdata.pickle', 'rb') as file:
        texts = pickle.load(file)
        lda = Lda()
        lda.train_lda(texts=texts, num_topics=10)
        lda.persist_lda()
        lda.visualize()
