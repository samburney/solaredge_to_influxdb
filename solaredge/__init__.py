import requests


class SolarEdge():
    def __init__(self, **kwargs):
        self.url = 'https://monitoringapi.solaredge.com/'
        if 'url' in kwargs:
            self.url = kwargs['url']

        self.site = None
        if 'site' in kwargs:
            self.site = kwargs['site']

        self.api_key = None
        if 'api_key' in kwargs:
            self.api_key = kwargs['api_key']

    def get_overview(self):
        uri = f'{self.url}/site/{self.site}/overview?api_key={self.api_key}'
        response = requests.get(uri)

        if response.status_code == 200:
            data = response.json()

            return data
        else:
            return False
