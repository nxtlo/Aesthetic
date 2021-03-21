class Friends:
    __slots__ = ('path', 'total')

    def __init__(self, data):
        self.path = data['friendslist'].get('friends')
        self.total = [f['steamid'] for f in self.path]


class User:
    __slots__= ('path' ,'id', 'name', 'url', 'avatar', 'clan_id', 'playing_now', 'country_flag', 'game_id')

    def __init__(self, data):
        self.path = data['response'].get("players")
        self.id = [s['steamid'] for s in self.path]
        self.playing_now = '\n'.join([s['gameextrainfo'] for s in self.path])
        self.country_flag = '\n'.join([s['loccountrycode'] for s in self.path])
        self.name = "\n".join([s['personaname'] for s in self.path])
        self.url = [s['profileurl'] for s in self.path]
        self.game_id = "\n".join([s['gameid'] for s in self.path])
        self.avatar = "\n".join([s['avatarfull'] for s in self.path])
        self.clan_id = [s['primaryclanid'] for s in self.path]