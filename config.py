import os


class Config:
    auth_token = os.getenv("NEWSMINER_AUTH_TOKEN")
    api_endpoint = 'https://newsbox.quving.com'
