import requests

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