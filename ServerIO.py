import mysql.connector
import re
from Trigger import Trigger
<<<<<<< HEAD
import json


class ServerIO:

    def __init__(self):
        with open("DatabaseConfig.json") as file:
            fileDic = json.load(file)
            self.host = fileDic["host"]
            self.user = fileDic["user"]
            self.pwd = fileDic["pwd"]
            self.databaseName = fileDic["db"]

        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            database=self.databaseName
        )

    def read_triggers(self, triggerIds):
        trigger_list = []
        read_in_triggerId = []

        cursor = self.db.cursor()
=======


def read_triggers(url, user, pwd, triggerIds):
    trigger_list = []
    read_in_triggerId = []

    db = mysql.connector.connect(
        host=url,
        user=user,
        password=pwd,
        database="ifttt"
    )
>>>>>>> parent of 0fe96a6... database config

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

<<<<<<< HEAD
    # Sanitize url to make it compatible to requests module
    def sanitize_url(self):
        url = self.host.strip('http://')
        url = url.strip('https://')
        return url

    def pushNotification(self, triggerId, owner, trigger):
=======
    print('Triggers Loaded')
    # time.sleep(10)
    return trigger_list, remove_triggers


# Sanitize url to make it compatible to requests module
def sanitize_url(url):
    url = url.strip('http://')
    url = url.strip('https://')
    return url

>>>>>>> parent of 0fe96a6... database config

def pushNotification(url, user, pwd, triggerId, owner, trigger):
    db = mysql.connector.connect(
        host=url,
        user=user,
        password=pwd,
        database="ifttt"
    )

    cursor = db.cursor()

    cursor.execute("SELECT * FROM triggers where trigger_id = %s", (triggerId,))

<<<<<<< HEAD
        if cursor.fetchone() is not None:
            cursor.execute("INSERT IGNORE INTO pending_notifications VALUES (%s, %s, %s)",
                           (str(triggerId), str(trigger.condition_string), str(owner)))
=======
    if cursor.fetchone() is not None:

        cursor.execute("INSERT IGNORE INTO pending_notifications VALUES (%s, %s, %s)",
                       (str(triggerId), str(trigger.condition_string), str(owner)))
>>>>>>> parent of 0fe96a6... database config

    db.commit()

    print("added " + str(triggerId) + " to pending table")
