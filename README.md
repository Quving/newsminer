# Newsminer

## Description
As the name suggests, this repository contains scripts to analyze news articles. 
For the first, only German texts will be analyzed. These texts will be provided by the [Newsbox-Api](https://newsbox.quving.com), which will aggregate new news at regular intervals.
Goal is to obtain a LDA-Model that is capable of clustering the news.


## Setup

### Installation
Install the required dependencies by the following steps.
1. ```virtualenv -p $(which python3.6) venv```
2. ```source venv/bin/acticate```
3. ```pip install -r requirements.txt```


### Authentication
In order to retrieve articles stored in the Newsbox-API, credentials are required.
You can obtain them by mailing me (vinh-ngu@hotmail.com).

```
curl -X POST  \ 
    -H "accept: application/json" \
    -H "Content-Type: application/json" \ 
    -d "{ "username\": "string", "password\": "string"}" \
    https://newsbox.quving.com/auth/token/
```

Example Response:
```bash
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI0NiJ10.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsI2J...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI2NiJ10.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZX..."
}
```

Now set environment-variable to make it usable in the script.
```
export NEWSMINER_AUTH_TOKEN='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI2NiJ10.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZX...'
```
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

Output:

```heut sein ein wirklich lang tag sein der hund essen sein leckerli```

### Train LDA
- In order to train a LDA, the POS-Tagger is required (stored locally in ```.../artififacts/tagger/...```)
- Also, you need to have access to the Newsbox-API (see 'Authentication' section above.)
- Execute ```python train_lda.py```. It can take some minutes depending on if you're using cached files or not.
- If it's done, the browser should open up automatically.


## Approach
- If the tagger tag a word as noun, the original word will be taken instead of its stem.
- Only nouns will be respected for the lda-model.

### References
- https://datascience.blog.wzb.eu/2016/07/13/accurate-part-of-speech-tagging-of-german-texts-with-nltk/ 
- https://towardsdatascience.com/topic-modeling-and-latent-dirichlet-allocation-in-python-9bf156893c24


## Troubleshooting
### Mysql - Problems (Mac)
```
...

  copying MySQLdb/constants/FIELD_TYPE.py -> build/lib.macosx-10.9-x86_64-3.6/MySQLdb/constants
  copying MySQLdb/constants/FLAG.py -> build/lib.macosx-10.9-x86_64-3.6/MySQLdb/constants
  running build_ext
  building 'MySQLdb._mysql' extension
  creating build/temp.macosx-10.9-x86_64-3.6
  creating build/temp.macosx-10.9-x86_64-3.6/MySQLdb
  gcc -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -arch x86_64 -g -Dversion_info=(1,4,6,'final',0) -D__version__=1.4.6 -I/usr/local/Cellar/mysql/8.0.19/include/mysql -I/Library/Frameworks/Python.framework/Versions/3.6/include/python3.6m -c MySQLdb/_mysql.c -o build/temp.macosx-10.9-x86_64-3.6/MySQLdb/_mysql.o
  gcc -bundle -undefined dynamic_lookup -arch x86_64 -g build/temp.macosx-10.9-x86_64-3.6/MySQLdb/_mysql.o -L/usr/local/Cellar/mysql/8.0.19/lib -lmysqlclient -lssl -lcrypto -o build/lib.macosx-10.9-x86_64-3.6/MySQLdb/_mysql.cpython-36m-darwin.so
  ld: library not found for -lssl
  clang: error: linker command failed with exit code 1 (use -v to see invocation)
  error: command 'gcc' failed with exit status 1
  ----------------------------------------
  ERROR: Failed building wheel for mysqlclient
```
Some pip dependencies require the mysql_config. Thus, following fix can be applied:

```
brew install mysql-client
brew install openssl
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
```

