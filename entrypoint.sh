#!/bin/bash
set -e

echo "Download assets..."
python setup.py

echo "Download pre-trained german pos-tagger from minio.quving.com..."
mkdir -p artifacts/tagger
curl -X GET "https://minio.quving.com/newsbox/tagger_de.pickle" --output "artifacts/tagger/tagger_de.pickle"

echo "Train and update LDA-Model."
python train_lda.py
