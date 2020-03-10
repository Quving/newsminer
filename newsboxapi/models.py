class Article:
    def __init__(self, json):
        self.author = json['author']
        self.content = json['content']
        self.created = json['created']
        self.description = json['description']
        self.publishedAt = json['publishedAt']
        self.source = json['source']
        self.title = json['title']
        self.url = json['url']
        self.urlToImage = json['urlToImage']
