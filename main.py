#!python
import os
import sys
import requests
from pyfzf.pyfzf import FzfPrompt

# Config
URLTS = 'http://127.0.0.0:8090'  # TorrServer URL
TSUser = ''  # TorrServer username
TSPass = ''  # TorrServer password
URLJAC = 'https://example.com'  # Jackett URL
APIKEY = ''  # Api key for jackett
PLAYER = '/bin/mpv'  # Path to media-player
fzf = FzfPrompt('/bin/fzf')  # Path to FZF


class TorrServer:
    def __init__(self, ip):
        self.ip = ip

    def __str__(self):
        return requests.get(f'{self.ip}/echo', auth=(TSUser, TSPass)).text

    def torrents(self):
        req = requests.post(f'{self.ip}/torrents', json={'action': 'list'}, auth=(TSUser, TSPass))
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
                                                   }, auth=(TSUser, TSPass))


class Jackett:
    def __init__(self, url, apikey):
        self.url = url
        self.apikey = apikey

    def search(self, query):
        parameters = {
            'apikey': self.apikey,
            'Query': query
        }
        req = requests.get(f'{self.url}/api/v2.0/indexers/all/results', params=parameters)
        return req.json()


def fzf_torrent(torrent_list):
    titles = []
    for i in torrent_list:
        titles.append(i['title'])
    res = fzf.prompt(titles)
    for i in torrent_list:
        if i['title'] == res[0]:
            return i


def fzf_jac_search(torrent_list):
    titles = []
    for i in torrent_list['Results']:
        titles.append(i['Title'])
    res = fzf.prompt(titles)
    for i in torrent_list['Results']:
        if i['Title'] == res[0]:
            return i


def view_torrents(start):
    hash_torrent = fzf_torrent(ts.torrents())['hash']
    if start:
        link_m3u = ts.torrent_m3u_url(hash_torrent, False)
    else:
        link_m3u = ts.torrent_m3u_url(hash_torrent)
    os.system(f'{PLAYER} \'{link_m3u}\'')


def jackett_search(query):
    jackett = Jackett(URLJAC, APIKEY)
    hash_torrent = fzf_jac_search(jackett.search(query))['MagnetUri']
    ts.torrent_add(hash_torrent)
    link_m3u = ts.torrent_m3u_url(hash_torrent)
    os.system(f'{PLAYER} \'{link_m3u}\'')


if __name__ == '__main__':
    ts = TorrServer(URLTS)

    if len(sys.argv) == 2:
        if sys.argv[1] == '-s':
            view_torrents(True)
        else:
            jackett_search(sys.argv[1])
    elif len(sys.argv) > 2:
        print('unknown parameters')
    elif len(sys.argv) == 1:
        view_torrents(False)
