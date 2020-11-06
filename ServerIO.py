import mysql.connector
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
        (owner, name, trigger_id, monitor_type, condition, severity, url, message) = t
        trigger = Trigger(url, monitor_type, condition, severity)

        trigger_list.append(trigger)

    return trigger_list


def notify_api(url, user, pwd):
    pass
