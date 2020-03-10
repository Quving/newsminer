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
- Finally execute ``` python train_tagger_de.py ``` It will store the tagger in picke-format to 
```[repo]/artifacts/tagger/```
 
 
