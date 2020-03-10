#!/usr/bin/python
import queue
from threading import Thread

import progressbar
from pattern.text.de import singularize, conjugate, predicative

from preprocessing.tagger import Tagger


class Lemmatizer():
    def __init__(self):
        self.tagger = Tagger()
        self.tagger.load_tagger()

    def lemmatize_word(self, word, pos):
        """
        Returns a stemming of a given word and its pos.
        :param word:
        :param pos:
        :return:
        """
        if pos.startswith('NN'):  # singularize noun
            return singularize(word)
        elif pos.startswith('V'):  # get infinitive of verb
            return conjugate(word)
        elif pos.startswith('ADJ') or pos.startswith('ADV'):  # get baseform of adjective or adverb
            return predicative(word)
        return word

    def lemmatize_text(self, text, lower=True, verbose=False):
        """
        Lemmatizes a given text.
        :param text:
        :return:
        """
        # Split the text into sentences to get rid of the punctuation.
        sentences = text.split(".")
        output = list()
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:  # If sentence is not empty.
                tagged_text = self.tagger.tag(text=sentence.split(' '))  # Output [(token, pos)]
                for word, pos in tagged_text:
                    token = self.lemmatize_word(word, pos)
                    if verbose:
                        print("{} -> {} ({})".format(word, token, pos))
                    output.append(token.lower() if lower else token)
        return ' '.join(output)

    def worker(self, queue):
        xs = queue.get()

        out = list()
        for i in xs:
            self.counter += 1
            self.bar.update(self.counter)
        queue.task_done()

    def lemmatize(self, n_threads, data):
        self.counter = 0
        self.bar = progressbar.ProgressBar(max_value=len(data))

        to_compute_splitted = self.split(data, n_threads)

        q = queue.Queue()
        for i in range(n_threads):
            t = Thread(target=self.worker, args=(q,))
            t.start()

        for sublist in to_compute_splitted:
            q.put(sublist)

        q.join()
