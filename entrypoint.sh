#!/bin/bash
set -e
echo "Download pre-trained german pos-tagger from minio.quving.com..."
mkdir -p data
curl -X GET "https://minio.quving.com/newsbox/tagger_de.pickle" --output "data/tagger_de.pickle"

echo "Train and update LDA-Model."
python train_lda.py
