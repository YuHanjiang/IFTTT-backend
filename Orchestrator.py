import threading
import json
import ServerIO

from Relation import Relation
from Trigger import Trigger
from OutputSource import OutputSource
from Monitor import Monitor

url = ''

api_url = '127.0.0.1'
api_user = 'root'
api_pwd = '63MH0UT7DCW30'


# Code below is used to send relation's output to the server
# @todo
# output_json = relation.outputSource.make_json()
# ServerIO.send_server_request(url, output_json)


class Orchestrator:
    def __init__(self):
        self.checkers = []  # collection of threads that will run checker functions
        self.relations = []  # relations

        self.testCheckerItem = 0

    # create and start threads for each each relation with appropriate checker function
    def start_monitors(self):
        for relation in self.relations:
            checker = Monitor(relation)
            self.checkers.append(threading._start_new_thread(checker.start, ()))
            

def __main__():
    orchestrator = Orchestrator()
    trigger_list = ServerIO.read_triggers(api_url, api_user, api_pwd)
    orchestrator.start_checkers()


__main__()
