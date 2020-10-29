import requests
from pythonping import ping
from pymongo import MongoClient
import importlib


def show_mongo():
    client = MongoClient('vocation.cs.umd.edu', 27017)
    db = client.IFTTT_database
    information = db.information
    cursor = information.find({})
    for c in cursor:
        print(c)


def add_mongo(name, message):
    client = MongoClient('vocation.cs.umd.edu', 27017)
    db = client.IFTTT_database
    information = db.information
    entry = {'name': name, 'message': message}
    x = information.insert_one(entry)
    print(x)


def get_requests(url):
    # Get http request from given url
    r = requests.get(url)

    print(r.status_code)
    print(r.headers['content-type'])
    if r.status_code == requests.codes.ok:
        json_response = r.json()
        print(json_response['result'])
        for ele in json_response['result']:
            print(ele['message'])


def ping_website(url, size):
    response = ping(url, size=size)
    print(response.rtt_avg_ms)


def http_heal_check(url):
    r = requests.get(url)
    # Check status code of http request
    if r.status_code == requests.codes.ok:
        return True
    else:
        return False

# ping_website('8.8.8.8', 40)

# get_requests('http://vocation.cs.umd.edu/flask/helloworld/')

