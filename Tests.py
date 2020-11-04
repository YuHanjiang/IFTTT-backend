import requests
from pythonping import ping
import mysql.connector
import importlib


def mysql_request():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="63MH0UT7DCW30",
        database="ifttt",
        auth_plugin='mysql_native_password'
    )
    print(mydb)

    cursor = mydb.cursor()

    cursor.execute("Select * from triggers")

    result = cursor.fetchall()
    for r in result:
        print(r)


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

mysql_request()