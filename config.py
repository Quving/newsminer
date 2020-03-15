import logging
import os


class Config:
    # NewsboxApi configuration
    auth_token = os.getenv("NEWSMINER_AUTH_TOKEN")
    api_endpoint = 'https://newsbox.quving.com'

    # Tagger
    tagger_storage_path = 'artifacts/tagger'

    # Lda
    lda_storage_path = 'artifacts/lda'

    # Minio S3
    minio_host = os.getenv("NEWSMINER_MINIO_HOST", "")
    minio_access_key = os.getenv("NEWSMINER_MINIO_ACCESS_KEY", "")
    minio_secret_key = os.getenv("NEWSMINER_MINIO_SECRET_KEY", "")


class Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
