import re
import time
import ServerIO

api_url = '127.0.0.1'
api_user = 'root'
# api_pwd = ''
api_pwd = '63MH0UT7DCW30'

# abstract Monitor class to be implemented in the backend of IFTTT
class Monitor:

    # Initialize Monitor object and input the trigger

    def run(self):
        self._dicParser()
        while not self.trigger.terminated:
            result = False
            for i in range(len(self.funcList)):
                # if self.funcList[i](self.paraList[i][0], self.paraList[i][1]):
                #     self.conditionMet = True
                #     print(self.triggerId, 'Notify Server', sep=' ')
                #
                # else:
                #     print(self.triggerId, 'Satisfy', sep=' ')
                result = result or self.funcList[i](self.paraList[i][0], self.paraList[i][1])
            if result:
                print(self.triggerId, 'Alert', sep=' ')
                ServerIO.pushNotification(api_url, api_user, api_pwd, self.triggerId, self.trigger_owner, self.trigger)
                time.sleep(self.refresh_time)
            else:
                print(self.triggerId, 'Passed', sep=' ')
                time.sleep(self.interval)

    def __init__(self, trigger):
        self.conditionMet = False

        if trigger is not None:
            self.trigger = trigger
            self.refresh_time = 60
            self.triggerId = trigger.trigger_id
            self.src = trigger.src
            self.conditions = trigger.condition
            self.trigger_owner = trigger.owner
            if 'Interval' not in self.conditions.keys():
                self.interval = 5
            else:
                self.interval = self.conditions['Interval']

        self.funcList = []
        self.paraList = []

    def _mapper(self):
        return []

    def _dicParser(self):
        funcs = self._mapper()

        for key in self.conditions.keys():
            self.funcList.append(funcs[key])

        for value_lists in self.conditions.values():
            for value in value_lists:
                cmpFun = None
                val = None
                reg = re.match(r'([<>=][<>=])([0-9]+)', value)
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
                    reg = re.match(r'^(\d+) - (\d+)$', value)
                    if reg is not None:
                        f = reg.group(1)
                        last = reg.group(2)
                        val = (float(f), float(last))
                        if f is not None and last is not None:
                            cmpFun = self.between

                if cmpFun:
                    self.paraList.append((cmpFun, val))

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

# PUBLIC FUNCTIONS
