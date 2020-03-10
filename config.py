import os


class Config:
    # NewsboxApi configuration
    auth_token = os.getenv("NEWSMINER_AUTH_TOKEN")
    api_endpoint = 'https://newsbox.quving.com'

    # Tagger
    tagger_storage_path = 'artifacts/tagger'

    # Lda
    lda_storage_path = 'artifacts/lda'
