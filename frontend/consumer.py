import requests
import os

API_BASE = 'http://0.0.0.0:5003'

class TrinitClient(object):

    def __init__(self):

        self.api_base = API_BASE

    def process_get(self, url):

        final_url = self.api_base + url

        resp = requests.get(final_url)
        print("url",final_url)
        print(resp)
        return resp.json()

    def process_post(self, url, data):

        final_url = self.api_base + url

        print(final_url)

        resp = requests.post(final_url, json = data)
       
        return resp.json()