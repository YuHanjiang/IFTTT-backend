import mysql.connector
import re
from Trigger import Trigger


def read_triggers(url, user, pwd, triggerIds):
    trigger_list = []
    read_in_triggerId = []

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
        read_in_triggerId.append(trigger_id)
        # dont add triggers that are already in the system
        if trigger_id not in triggerIds:

            # Parse condition data
            cond = re.search(r'^(.*): (.*)$', condition)
            if cond is not None:
                test_method = cond.group(1)
                test_values = cond.group(2)
                if test_method == 'Latency':
                    trigger_condition[test_method] = ['>=' + test_values]
                elif test_method == 'Status code':
                    test_values = test_values.split(', ')
                    trigger_condition[test_method] = ['==' + t for t in test_values]

                url = sanitize_url(url)

                trigger = Trigger(trigger_id, url, monitor_type, trigger_condition, severity, owner, condition)

                trigger_list.append(trigger)

    remove_triggers = [t_id for t_id in triggerIds if t_id not in read_in_triggerId]

    print('Triggers Loaded')
    # time.sleep(10)
    return trigger_list, remove_triggers


# Sanitize url to make it compatible to requests module
def sanitize_url(url):
    url = url.strip('http://')
    url = url.strip('https://')
    return url


def pushNotification(url, user, pwd, triggerId, owner, trigger):
    db = mysql.connector.connect(
        host=url,
        user=user,
        password=pwd,
        database="ifttt"
    )

    cursor = db.cursor()

    # query = "INSERT IGNORE INTO pending_notifications (trigger_id) Values (" + str(triggerId) + "," + \
    #         str(trigger.condition) + "," + str(owner) + ") ON DUPLICATE KEY UPDATE "

    cursor.execute("INSERT IGNORE INTO pending_notifications VALUES (%s, %s, %s)",
                   (str(triggerId), str(trigger.condition_string), str(owner)))
    db.commit()
    print("added to pending table")
