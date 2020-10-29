import threading
import time
import json
import ServerIO

from Relation import Relation
from Trigger import Trigger
from OutputSource import OutputSource
from Checker import Checker 
from WebsiteHealthChecker import WebsiteHealthChecker

url = ''


def sendTriggerID(trigger):
    print(trigger.text)

    # Code below is used to send relation's output to the server
    # @todo
    # output_json = relation.outputSource.make_json()
    # ServerIO.send_server_request(url, output_json)


class Cycler:
    def __init__(self):
        self.checkers = []  # collection of threads that will run checker functions 
        self.checkersThreads = []
        self.triggers = []  # relations

        self.testCheckerItem = 0

    def read_json(self, relationsDB):

        for t in relationsDB:

            trigger = Trigger(src=t['src'], checker=t['checker'], conditions= t['conditions'], interval=t['interval'], id=t['id'], text=t['text'])

            self.triggers.append(trigger)

    # creates the relation objects based off of the database form sever-admin side
    def load_from_dataBase(self):
        with open("testDB/testRelations.json") as file:
            relationsDB = json.load(file)

            self.read_json(relationsDB)

        print("relations loaded")

    def load_data_from_server(self):
        relationsDB = ServerIO.get_server_request(url)
        self.read_json(relationsDB)

    # create and start threads for each each relation with appropriate checker function
    def start_checkers(self):
        for trigger in self.triggers: 
            if trigger.checker == "WebsiteHealthChecker": 
                checker = WebsiteHealthChecker(trigger) 
            checker.mapper()  
            self.checkers.append(checker)
            self.checkersThreads.append(threading._start_new_thread(checker.run, ()))

    # checks the relations to see if any have been set to true then sends output src
    def monitor(self):
        while True:
            length = range(len(self.triggers))
            for i in length:
                if self.checkers[i].conditionMet:
                    sendTriggerID(self.triggers[i])
                    self.checkers.pop(i)
                    self.checkersThreads.pop(i)
                    self.triggers.pop(i)
                    length = range(len(self.checkers))
            print("NEXT CHECK")

            time.sleep(0.5)


# def testChecker(relation):
#     while True:
#         if 5 > 10:
#             relation.isPulled = True
#             break
#         time.sleep(0.5)


cycler = Cycler()
cycler.load_from_dataBase()
cycler.start_checkers()
cycler.monitor()
