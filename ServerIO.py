import requests


def get_server_request(url):
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
        return r.json()


def send_server_request(url, json):
    requests.post(url, json=json)
