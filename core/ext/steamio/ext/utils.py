

class VAC:
    __slots__ = ('meth', 'id', 'community', 'vac', 'count', 'last_ban', 'game_bans', 'economy_ban')

    def __init__(self, data):
        self.meth = [*data['players']]
        self.id = '\n'.join([v['SteamId'] for v in self.meth])
        self.community = [v['CommunityBanned'] for v in self.meth]
        self.vac = [v['VACBanned'] for v in self.meth]
        self.count = [v['NumberOfVACBans'] for v in self.meth]
        self.last_ban = [v['DaysSinceLastBan'] for v in self.meth]
        self.game_bans = [v['NumberOfGameBans'] for v in self.meth]
        self.economy_ban = [v['EconomyBan'] for v in self.meth]


class LastPlayed:
    __slots__ = ('meth', 'id', 'total_games', 'name', 'last_two_weeks', 'all_time', 'icon_url')
    HASH = 'http://media.steampowered.com/steamcommunity/public/images/apps'

    def __init__(self, data):
        self.meth = data['response'].get('games')
        self.id = [s['appid'] for s in self.meth]
        self.total_games = data['response'].get('total_count')
        self.last_two_weeks = [a['playtime_2weeks'] // 60 for a in self.meth]
        self.all_time = [a['playtime_forever'] for a in self.meth]
        self.name = [s['name'] for s in self.meth]
        self.icon_url = [f"{self.HASH}/{self.id}/{icon['img_icon_url']}.jpg" for icon in self.meth]
