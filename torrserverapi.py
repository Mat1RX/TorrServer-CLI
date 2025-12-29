import requests

class TorrServer:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password

    def __str__(self):
        return requests.get(f'{self.ip}/echo', auth=(self.user, self.password)).text

    def torrents(self):
        req = requests.post(f'{self.ip}/torrents', json={'action': 'list'}, auth=(self.user, self.password))
        return req.json()

    def torrent_m3u_url(self, torrent_hash, from_last=True):
        if from_last:
            return f'{self.ip}/stream/fname?link={torrent_hash}&index=1&m3u&fromlast'
        else:
            return f'{self.ip}/stream/fname?link={torrent_hash}&index=1&m3u'

    def torrent_add(self, torrent_hash):
        requests.post(f'{self.ip}/torrents', json={'action': 'add',
                                                   'link': torrent_hash,
                                                   'poster': '',
                                                   'save_to_db': True,
                                                   'title': '',
                                                   }, auth=(self.user, self.password))
