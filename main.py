#!python
import os
import sys
from pyfzf.pyfzf import FzfPrompt
from torrserverapi import TorrServer
from jackettapi import Jackett
from configuration import Configuration
default_configuration_file_name = 'config.yaml'

#init configuration
config = Configuration(default_configuration_file_name)

fzf = FzfPrompt('/bin/fzf')  # Path to FZF

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
    os.system(f'{config.PLAYER} \'{link_m3u}\'')


def jackett_search(query):
    jackett = Jackett(config.URLJAC, config.APIKEY)
    hash_torrent = fzf_jac_search(jackett.search(query))['MagnetUri']
    ts.torrent_add(hash_torrent)
    link_m3u = ts.torrent_m3u_url(hash_torrent)
    os.system(f'{config.PLAYER} \'{link_m3u}\'')


if __name__ == '__main__':
    ts = TorrServer(config.URLTS, config.TSUser, config.TSPass)

    if len(sys.argv) == 2:
        if sys.argv[1] == '-s':
            view_torrents(True)
        else:
            jackett_search(sys.argv[1])
    elif len(sys.argv) > 2:
        print('unknown parameters')
    elif len(sys.argv) == 1:
        view_torrents(False)
