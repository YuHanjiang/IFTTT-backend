import re
import time
from ServerIO import ServerIO


# abstract Monitor class to be implemented in the backend of IFTTT
class Monitor:

    # Initialize Monitor object and input the trigger

    def run(self):
        self._dicParser()
        print(self.funcList)
        while not self.trigger.terminated:
            # check wether trigger is active or not
            active = self.serverIO.checkIfActive(self.trigger.trigger_id)
            result = False
            for i in range(len(self.funcList)):
                funClause = self.funcList[i]
                paraClause = self.paraList[i]
                clauseResult = True
                for j in range(len(funClause)):
                    clauseResult = clauseResult and funClause[j](paraClause[j][0], paraClause[j][1])
                result = result or clauseResult

            if result:
                # if it is active sound alarm
                if active == 1:
                    print(self.triggerId, 'Alert', sep=' ')
                    self.serverIO.pushNotification(self.triggerId, self.trigger_owner, self.trigger)
                    # active = 0
            else:
                # if not active switch back to active
                if active == 0:
                    self.serverIO.setBackToActive(self.triggerId)
                print(self.triggerId, 'Passed', sep=' ')
            time.sleep(self.interval)

    def __init__(self, trigger):
        self.conditionMet = False
        self.serverIO = ServerIO()

        if trigger is not None:
            self.trigger = trigger
            self.refresh_time = 60
            self.triggerId = trigger.trigger_id
            self.src = trigger.src
            self.conditions = trigger.condition
            self.trigger_owner = trigger.owner
            self.interval = trigger.interval

        self.funcList = []
        self.paraList = []

    def _mapper(self):
        return []

    def _dicParser(self):
        funcs = self._mapper()

        for clause in self.conditions:
            clauseFuns = []
            clausePara = []
            for var, cond in clause:
                clauseFuns.append(funcs[var])
                cmpFun = None
                val = None

                reg = re.match(r'(>=|<=|==|!=|<|=|>|contains|does not contain)([0-9]+)', cond)
                if reg is not None:
                    clause = reg.group(1)
                    val = float(reg.group(2))

                    if clause is not None and val is not None:
                        if clause == "==" or clause == "=":
                            cmpFun = self.equal_equal
                        elif clause == ">=":
                            cmpFun = self.greater_equal
                        elif clause == "<=":
                            cmpFun = self.lesser_equal
                        elif clause == ">":
                            cmpFun = self.greater
                        elif clause == "<":
                            cmpFun = self.lesser

                clausePara.append((cmpFun, val))
            self.funcList.append(clauseFuns)
            self.paraList.append(clausePara)

        # for string in self.conditions.values():
        #     cmpFun = None
        #     val = None
        #     reg = re.match(r'([<>=][<>=])([0-9]*|[0-9]*.[0.9]*)', string)
        #     if reg is not None:
        #         clause = reg.group(1)
        #         val = float(reg.group(2))
        #
        #         if clause is not None and val is not None:
        #             if clause == "==":
        #                 cmpFun = self.equal_equal
        #             elif clause == ">=":
        #                 cmpFun = self.greater_equal
        #             elif clause == "<=":
        #                 cmpFun = self.lesser_equal
        #     else:
        #         reg = re.match(r'^(\d+) - (\d+)$', string)
        #         if reg is not None:
        #             f = reg.group(1)
        #             last = reg.group(2)
        #             val = (float(f), float(last))
        #             if f is not None and last is not None:
        #                 cmpFun = self.between
        #
        #     if cmpFun:
        #         self.paraList.append((cmpFun, val))

    # Start the Monitor and check what is the method of checking
    # The method returns true if the check satisfies the user's defined condition
    @staticmethod
    def between(a, b):
        (f, l) = b
        if f <= a <= l:
            return True
        else:
            return False

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
    @staticmethod
    def greater(a, b):
        return a > b

    @staticmethod
    def lesser(a, b):
        return a < b

    @staticmethod
    def greater(a, b):
        return a > b

    @staticmethod
    def lesser(a, b):
        return a < b

# PUBLIC FUNCTIONS
