
class App:
    __slots__ = ('path', 'ext' ,'id', 'title', 'url', 'author', 'content')

    def __init__(self, data):
        self.path = data.get("appnews")
        self.ext = self.path.get('newsitems')
        self.id = self.path.get('appid')
        super().__init__()