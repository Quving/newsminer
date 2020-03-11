# Newsminer

## Description
As the name suggests, this repository contains scripts to analyze news articles. 
For the first, only German texts will be analyzed. These texts will be provided by the [Newsbox-Api](https://newsbox.quving.com), which will aggregate new news at regular intervals.
Goal is to obtain a LDA-Model that is capable of clustering the news.


## Setup
Install the required dependencies by the following steps.
1. ```virtualenv -p $(which python3.6) venv```
2. ```source venv/bin/acticate```
3. ```pip install -r requirements.txt```

## Documentation
### Train german POS-Tagger
The German POS Tagger is required for the lemmatization and stemming. That is a necessary step for the data preprocessing
in order to train a LDA-Model.

- To do that, you need to download the trainingset first. I recommend to use 
'[tiger_release_aug07.corrected.16012013.conll09](https://www.ims.uni-stuttgart.de/documents/ressourcen/korpora/tiger-corpus/download/start.html)'
 that is provided by the University of Stuttgart.
- Once downloaded, create a directory 'data' and move the downloaded file to that directory.
- Finally execute ``` python train_tagger_de.py ``` It will store the tagger in pickle-format to 
```[repo]/artifacts/tagger/```

#### References
https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/ 
 
### Stemming/Lemmatization
Example snippet.
```
from lemmatizer import Lemmatizer

if __name__ == '__main__':
    lemmatizer = Lemmatizer()
    text = "Heute war ein wirklich langer Tag gewesen. Der Hund isst sein Leckerli."
    text = lemmatizer.lemmatize_text(text=text)
    print(text)
```

output:

```heut sein ein wirklich lang tag sein der hund essen sein leckerli```

### Train LDA
- In order to train a LDA, the POS-Tagger is required (stored locally in ```.../artififacts/tagger/...```)
- Execute ```python train_lda.py```. It can take some minutes depending on if you're using cached files or not.
- If it's done, the browser should open up automatically.


## Approach
- If the tagger tag a word as noun, the original word will be taken instead of its stem.
- Only nouns will be respected for the lda-model.