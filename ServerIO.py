import mysql.connector
import re
from Trigger import Trigger
import json


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
            (name, monitor_type, severity, url, message, trigger_id, condition, owner, active, interval) = t
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
                                      condition, interval)

                    trigger_list.append(trigger)

        remove_triggers = [t_id for t_id in triggerIds if t_id not in read_in_triggerId]

        print('Triggers Loaded')
        # time.sleep(10) 
        return trigger_list, remove_triggers

    # Sanitize url to make it compatible to requests module

    def pushNotification(self, triggerId, owner, trigger, clause_list):

        cursor = self.db.cursor()

        # Adding all the conditions that are met into the pending_notifications
        s = ""

        for cl in clause_list:
            for con in cl:
                (comp, val) = con
                s += str(comp) + str(val) + ","
        s = s[:-1]
        cursor.execute("SELECT * FROM triggers where trigger_id = %s", (triggerId,))

        if cursor.fetchone() is not None:
            cursor.execute("INSERT IGNORE INTO pending_notifications VALUES (%s, %s, %s)",
                           (str(triggerId), str(s), str(owner)))

        self.db.commit()

        print("added " + str(triggerId) + " to pending table")

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
