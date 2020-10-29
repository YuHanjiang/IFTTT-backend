import re
import requests
import time
import ServerIO


# abstract Monitor class to be implemented in the backend of IFTTT
class Monitor:

    # Initialize Monitor object and input the trigger
    def __init__(self, trigger):
        self.conditionMet = False

        if trigger is not None:
            self.triggerId = trigger.id
            self.src = trigger.src
            self.method = trigger.method
            self.conditions = trigger.conditions
            self.interval = trigger.interval

        self.funcList = []
        self.paraList = []

    def _mapper(self):
        pass

    def _dicParser(self):
        funcs = self._mapper()

        for key in self.conditions.keys():
            self.funcList.append(funcs[key])

        for string in self.conditions.values():
            reg = re.match("([<>=][<>=])([0-9]*|[0-9]*.[0.9]*)", string)
            clause = reg.group(1)
            val = float(reg.group(2))

            cmpFun = None

            if clause == "==":
                cmpFun = self.equal_equal
            elif clause == ">=":
                cmpFun = self.greater_equal
            elif clause == "<=":
                cmpFun = self.lesser_equal

            if cmpFun:
                self.paraList.append((cmpFun, val))

    # Start the Monitor and check what is the method of checking
    # The method returns true if the check satisfies the user's defined condition

    @staticmethod
    def equal_equal(a, b):
        if a == b:
            return True
        else:
            return False

    @staticmethod
    def greater_equal(a, b):
        if a >= b:
            return True
        else:
            return False

    @staticmethod
    def lesser_equal(a, b):
        if a <= b:
            return True
        else:
            return False


# PUBLIC FUNCTIONS
def run(self):
    self._dicParsaer(self)

    while True:

        for i in range(len(self.funcList)):
            if self.funcList[i](self.paraList[i][0], self.paraList[i][1]):
                self.conditionMet = True
                break

        time.sleep(self.interval)
