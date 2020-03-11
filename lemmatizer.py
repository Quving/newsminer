#!/usr/bin/python

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
        output = list()
        text = " ".join([x for x in text.split() if x.isalnum()]).strip()
        tagged_text = self.tagger.tag(text=text.split(' '))  # Output [(token, pos)]
        exclude_pos = "N"
        for word, pos in tagged_text:
            token = self.lemmatize_word(word, pos)
            if verbose:
                print("{} -> {} ({})".format(word, token, pos))
            if pos.startswith(exclude_pos):
                output.append(token.lower() if lower else token)
            else:
                output.append(word.lower() if lower else word)
        return ' '.join(output)
