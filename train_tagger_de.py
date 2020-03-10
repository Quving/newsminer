from preprocessing.tagger import Tagger

if __name__ == '__main__':
    tagger_de = Tagger()
    tagger_de.train_tagger()
    tagger_de.persist_tagger()
