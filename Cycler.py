import threading
import time
import json
import ServerIO

from Relation import Relation
from Trigger import Trigger
from OutputSource import OutputSource
from Checker import Checker

url = ''


def sendOutputSource(relation):
    print(relation.outputSource.text)

    # Code below is used to send relation's output to the server
    # @todo
    # output_json = relation.outputSource.make_json()
    # ServerIO.send_server_request(url, output_json)


class Cycler:
    def __init__(self):
        self.checkers = []  # collection of threads that will run checker functions
        self.relations = []  # relations

        self.testCheckerItem = 0

    def read_json(self, relationsDB):

        for r in relationsDB:
            t = r['trigger']
            o = r['output']
            trigger = Trigger(t['src'], t['method'], t['condition'], t['interval'])
            output = OutputSource(o['text'], o['severity'], o['key'], o['audience'])

            relation = Relation(trigger, output)

            self.relations.append(relation)

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
        for relation in self.relations:
            checker = Checker(relation)
            self.checkers.append(threading._start_new_thread(checker.start, ()))

    # checks the relations to see if any have been set to true then sends output src
    def monitor(self):
        while True:
            length = range(len(self.relations))
            for i in length:
                if self.relations[i].isPulled:
                    sendOutputSource(self.relations[i])
                    self.relations.pop(i)
                    length = range(len(self.relations))
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
