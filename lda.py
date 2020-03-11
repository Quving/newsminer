import os
import pickle

import pyLDAvis.gensim
from gensim import corpora, models
from gensim.models import LdaMulticore
from gensim.models.ldamodel import LdaModel

from config import Config, Logger


class Lda():
    def __init__(self):
        self.logger = Logger.logger
        self.storage_path = Config.lda_storage_path

        # Filenames
        self.gensim_dictionary = 'dictionary.gensim'
        self.gensim_model = 'model.gensim'
        self.corpus_pickle = 'corpus.pkl'

    def persist_lda(self):
        """
        Persist corpus,dictionary and lda-model locally.
        :return:
        """
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        self.logger.info("Persist corpus, dictionary and lda-model to file.")
        pickle.dump(self.bow_corpus, open(os.path.join(self.storage_path, self.corpus_pickle), 'wb'))
        self.dictionary.save(os.path.join(self.storage_path, self.gensim_dictionary))
        self.ldamodel.save(os.path.join(self.storage_path, self.gensim_model))

    def load_lda(self):
        """
        Load corpus,dictionary and lda-model from local storage.
        :return:
        """
        self.logger.info("Loading corpus, dictionary and lda-model from file.")
        self.dictionary = corpora.Dictionary.load(os.path.join(self.storage_path, self.gensim_dictionary))
        self.bow_corpus = pickle.load((open(os.path.join(self.storage_path, self.corpus_pickle), "rb")))
        path = os.path.join(self.storage_path, self.gensim_model)
        self.ldamodel = LdaModel.load(path)

    def show_topics(self):
        topics = self.ldamodel.print_topics(num_words=5)
        for topic in topics:
            print(topic)

    def train_lda(self, texts, num_topics=5, n=None):
        self.logger.info("Create corpus, dictionary lda-model.")
        self.dictionary = corpora.Dictionary(texts)
        self.bow_corpus = [self.dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(self.bow_corpus)
        corpus_tfidf = tfidf[self.bow_corpus]

        self.ldamodel = LdaMulticore(
            corpus=corpus_tfidf,
            num_topics=num_topics,
            id2word=self.dictionary,
            passes=10,
            workers=3,
        )

    def classify(self, text):
        """
        Returns an vector of probabilities to which class the given text belongs to.
        :param text:
        :return:
        """
        self.logger.info("Classify the given text.")
        new_doc_bow = self.dictionary.doc2bow(text)
        return self.ldamodel.get_document_topics(new_doc_bow)

    def visualize(self):
        """
        Visualizes the lda-model usung LDAVIS.
        :return:
        """
        lda_display = pyLDAvis.gensim.prepare(
            self.ldamodel,
            self.bow_corpus,
            self.dictionary,
            sort_topics=True
        )
        pyLDAvis.show(lda_display)
