import os


class Config:
    # NewsboxApi configuration
    auth_token = os.getenv("NEWSMINER_AUTH_TOKEN")
    api_endpoint = 'https://newsbox.quving.com'
