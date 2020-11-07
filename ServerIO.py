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
        (owner, name, trigger_id, monitor_type, condition, severity, url, message) = t
        regex = '^(.+) (\\d) - (\\d)$'
        cond = re.search(regex, condition)
        trigger_condition = {cond.group(1): str('>=') + cond.group(2), cond.group(1): str('<=') + cond.group(3)}
        trigger = Trigger(trigger_id, url, monitor_type, trigger_condition, severity)

        trigger_list.append(trigger)

    print(trigger_list)
    return trigger_list


def notify_api(url, user, pwd):
    pass
