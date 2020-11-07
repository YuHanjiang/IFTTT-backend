import re
import time


# abstract Monitor class to be implemented in the backend of IFTTT
class Monitor:

    # Initialize Monitor object and input the trigger

    def run(self):
        self._dicParser()
        while True:
            for i in range(len(self.funcList)):
                if self.funcList[i](self.paraList[i][0], self.paraList[i][1]):
                    self.conditionMet = True
                    print(self.triggerId, 'Notify Server', sep=' ')

                else:
                    print(self.triggerId, 'Satisfy', sep=' ')

            time.sleep(self.interval)

    def __init__(self, trigger):
        self.conditionMet = False

        if trigger is not None:
            self.triggerId = trigger.trigger_id
            self.src = trigger.src
            self.conditions = trigger.condition
            if 'interval' not in self.conditions.keys():
                self.interval = 5
            else:
                self.interval = self.conditions['interval']

        self.funcList = []
        self.paraList = []

    def _mapper(self):
        pass

    def _dicParser(self):
        funcs = self._mapper()

        for key in self.conditions.keys():
            self.funcList.append(funcs[key])

        for string in self.conditions.values():
            cmpFun = None
            val = None
            reg = re.match("([<>=][<>=])([0-9]*|[0-9]*.[0.9]*)", string)
            if reg is not None:
                clause = reg.group(1)
                val = float(reg.group(2))

                if clause is not None and val is not None:
                    if clause == "==":
                        cmpFun = self.equal_equal
                    elif clause == ">=":
                        cmpFun = self.greater_equal
                    elif clause == "<=":
                        cmpFun = self.lesser_equal
            else:
                reg = re.match('^(\d+) - (\d+)$', string)
                if reg is not None:
                    f = reg.group(1)
                    l = reg.group(2)
                    val = (float(f), float(l))
                    if f is not None and l is not None:
                        cmpFun = self.between

            if cmpFun:
                self.paraList.append((cmpFun, val))

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

# PUBLIC FUNCTIONS
