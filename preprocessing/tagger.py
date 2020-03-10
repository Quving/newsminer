import os
import pickle
import random

import nltk

from preprocessing.classifierbasedgermantagger import ClassifierBasedGermanTagger
from config import Config


class Tagger():
    def __init__(self):
        self.storage_path = Config.tagger_storage_path
        self.tagger_path = 'tagger_de.pickle'

    def train_tagger(self):
        """
        Set a split size: use 90% for training, 10% for testing
        :return:
        """
        corp = nltk.corpus.ConllCorpusReader('data/', 'tiger_release_aug07.corrected.16012013.conll09',
                                             ['ignore', 'words', 'ignore', 'ignore', 'pos'],
                                             encoding='utf-8')

        tagged_sents = list(corp.tagged_sents())
        random.shuffle(tagged_sents)
        split_perc = 0.1
        split_size = int(len(tagged_sents) * split_perc)
        train_sents, test_sents = tagged_sents[split_size:], tagged_sents[:split_size]

        self.tagger_de = ClassifierBasedGermanTagger(train=train_sents)

    def tag(self, text):
        """
        Tag a given text.
        text = ['Das', 'ist', 'ein', 'einfacher', 'Test']
        :param text:
        :return:
        """
        return self.tagger_de.tag(text)

    def persist_tagger(self):
        """
        Persist the tagger to a local file.
        :return:
        """
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        pickle.dump(self.tagger_de, open(os.path.join(self.storage_path, self.tagger_path), 'wb'))

    def load_tagger(self):
        """
        Load the tagger from a local file.
        :return:
        """
        print(os.getcwd())
        self.tagger_de = pickle.load(open(os.path.join(self.storage_path, self.tagger_path), 'rb'))
