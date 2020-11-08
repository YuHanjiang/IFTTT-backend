import mysql.connector
import re
from Trigger import Trigger


def read_triggers(url, user, pwd):
    trigger_list = []

    db = mysql.connector.connect(
        host=url,
        user=user,
        password=pwd,
        database="ifttt"
    )

    cursor = db.cursor()

    cursor.execute('SELECT * FROM triggers')

    trigger_query = cursor.fetchall()
    for t in trigger_query:
        (name, monitor_type, severity, url, message, trigger_id, condition, owner) = t
        trigger_condition = {}

        # Parse condition data
        cond = re.search(r'^(.*): (.*)$', condition)
        if cond is not None:
            test_method = cond.group(1)
            test_values = cond.group(2)

            if test_method == 'latency':
                trigger_condition[test_method] = ['>=' + test_values[0]]
            elif test_method == 'Status Code':
                trigger_condition[test_method] = ['==' + t for t in test_values]

            url = sanitize_url(url)

            trigger = Trigger(trigger_id, url, monitor_type, trigger_condition, severity, owner)

            trigger_list.append(trigger)

    print('Triggers Loaded')
    return trigger_list


# Sanitize url to make it compatible to requests module
def sanitize_url(url):
    url = url.strip('http://')
    url = url.strip('https://')
    return 'http://' + url


def notify_api(url, user, pwd):
    pass
