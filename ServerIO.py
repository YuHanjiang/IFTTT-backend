import mysql.connector
import re
from Trigger import Trigger
import json
import requests


def sanitize_url(url):
    url = url.strip('http://')
    url = url.strip('https://')
    return url


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

        cursor.execute('SELECT * FROM triggers')

        trigger_query = cursor.fetchall()
        self.db.commit()

        # Getting the trigger_query
        for t in trigger_query:
            (name, monitor_type, severity, url, message, trigger_id, condition, owner, active, interval, port) = t
            read_in_triggerId.append(trigger_id)

            # dont add triggers that are already in the system
            if trigger_id not in triggerIds:
                # Parse condition data
                # Splitting conditions into clauses
                condition_clauses = condition.split('||')
                condition_list = []
                if condition_clauses is not None:
                    for clause in condition_clauses:
                        clause_list = []
                        # Split conditions into each sub-conditions (e.g. Status Code == 100)
                        sub_conditions = clause.split('&&')
                        if sub_conditions is not None:
                            for sub_cond in sub_conditions:
                                regex = r'([A-Za-z]+)(>=|<=|==|!=|<|=|>|contains|does not contain)(-?[0-9]+|\w+)'
                                cond = re.search(regex, sub_cond)
                                if cond is not None:
                                    test_method = cond.group(1)
                                    test_operator = cond.group(2)
                                    test_values = cond.group(3)
                                    # Append current condition into the list of conditions for the clause
                                    clause_list.append((test_method, test_operator + test_values))

                        # Append the current list of all conditions in a clause to the condition_list
                        condition_list.append(clause_list)

                    url = sanitize_url(url)
                    trigger = Trigger(trigger_id, url, monitor_type, condition_list, severity, owner,
                                      condition, interval, port, message)

                    trigger_list.append(trigger)

        remove_triggers = [t_id for t_id in triggerIds if t_id not in read_in_triggerId]
        new_trigger_ids = [t.trigger_id for t in trigger_list if t.trigger_id not in triggerIds]
        if len(new_trigger_ids) > 0:
            print('New Triggers: ', new_trigger_ids)
        if len(remove_triggers) > 0:
            print('Remove Triggers: ', remove_triggers)
        # time.sleep(10) 
        return trigger_list, remove_triggers

    # Sanitize url to make it compatible to requests module

    def pushNotification(self, trigger, s):

        cursor = self.db.cursor()

        # Adding all the conditions that are met into the pending_notifications
        cursor.execute("SELECT * FROM triggers where trigger_id = %s", (trigger.trigger_id,))

        # Without condition shows there is something wrong with the trigger
        if s == "":
            s = 'There is something wrong with your trigger testing. Please make sure you are creating the trigger as' \
                'specified'

        if cursor.fetchone() is not None:
            # cursor.execute("INSERT IGNORE INTO pending_notifications VALUES (%s, %s, %s)",
            #                (str(triggerId), str(s), str(owner)))
            cursor.execute('SELECT token FROM users where token is not null and users.username = %s', (trigger.owner,))

            token = cursor.fetchall()
            if token is not None:

                cursor.execute('SELECT os FROM users where os is not null and users.username = %s', (trigger.owner,))
                os = cursor.fetchall()
                if os is not None:
                    print(s)
                    self.send_fcm_notification(trigger, token, os, s)

    def send_fcm_notification(self, trigger, token, os, clause_string):
        try:
            dt_string = trigger.trigger_activation_date
            tm_string = trigger.trigger_activation_time
            os_string = os[0][0]
            to_send = None
            header_dict = {
                'Content-Type': 'application/json',
                'Authorization':
                    'key=AAAAtogJsGA:APA91bFlqRyTKH4zT1XOZt_RvWiXvzUhYJe3yoknalCI38S5RPsgu-RMXiAREKwnvZsnqDs8za_ECrTBzgT7lac2u17UP-0MKoJZyUX8pAFHcw8YhLI9g-TRcVS-71eXIVkUGE1H0Or6'
            }
            if os_string == 'ios':
                if int(trigger.severity) == 1:
                    to_send = {
                        "to": str(token[0][0]),
                        "collapse_key": "type_a",
                        "notification": {
                            "body": str(trigger.message),
                            "title": "IFTTT Trigger Notification"
                        },
                        "data": {
                            "trigger_date": str(dt_string),
                            "trigger_time": str(tm_string),
                            "trigger_id": str(trigger.trigger_id),
                            "conditions_met": str(clause_string),
                            "title": "IFTTT Trigger Notification",
                            "severity": str(trigger.severity)
                        }
                    }
                else:
                    to_send = {
                        "to": str(token[0][0]),
                        "collapse_key": "type_a",
                        "notification": {
                            "body": str(trigger.message),
                            "title": "IFTTT Trigger Notification",
                            "sound": "default"
                        },
                        "data": {
                            "trigger_date": str(dt_string),
                            "trigger_time": str(tm_string),
                            "trigger_id": str(trigger.trigger_id),
                            "conditions_met": str(clause_string),
                            "title": "IFTTT Trigger Notification",
                            "severity": str(trigger.severity)
                        }
                    }
            elif os_string == 'android':
                to_send = {
                    "to": str(token[0][0]),
                    "collapse_key": "type_a",
                    "data": {
                        "trigger_date": str(dt_string),
                        "trigger_time": str(tm_string),
                        "trigger_id": str(trigger.trigger_id),
                        "conditions_met": str(clause_string),
                        "title": "IFTTT Trigger Notification",
                        "severity": str(trigger.severity)
                    }
                }
            active = int(self.checkIfActive(trigger.trigger_id))
            if active and to_send is not None:
                requests.post('https://fcm.googleapis.com/fcm/send', headers=header_dict, json=to_send)
                print("Send ", trigger.trigger_id," Post Requests to FCM")
        except requests.exceptions.RequestException:
            print('Contact API')

    def checkIfActive(self, triggerID):

        cursor = self.db.cursor()
        cursor.execute("select trigger_status from triggers where trigger_id = " + str(triggerID))
        val = cursor.fetchall()[0][0]
        self.db.commit()
        return val

    def setBackToActive(self, triggerID):
        cursor = self.db.cursor()
        cursor.execute("update triggers set trigger_status = 1 where trigger_id = " + str(triggerID))
        self.db.commit()
