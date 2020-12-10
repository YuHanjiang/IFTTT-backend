import re
import time
from ServerIO import ServerIO
from datetime import datetime


# abstract Monitor class to be implemented in the backend of IFTTT
class Monitor:

    # Initialize Monitor object and input the trigger

    def run(self):
        self._dicParser()
        while not self.trigger.terminated:
            # check whether trigger is active or not
            active = int(self.serverIO.checkIfActive(self.trigger.trigger_id))
            result = False
            # Adding a list to track all clause conditions that are actually met
            clause_met = []
            for i in range(len(self.funcList)):
                funClause = self.funcList[i]
                paraClause = self.paraList[i]
                clauseResult = True
                condition_met_string = ""
                for j in range(len(funClause)):
                    try:
                        current_result, real_value = funClause[j](paraClause[j][0], paraClause[j][1])
                        clauseResult = clauseResult and current_result
                        par, val_st = self.trigger.condition[i][j]
                        if current_result:
                            condition_met_string += par + '(' + str(real_value) + ')' + val_st + ','
                    # Handling url error
                    except ValueError:
                        self.trigger.terminated = True
                        print('URL Error: ', self.triggerId)
                        self.serverIO.pushNotification(self.trigger, 'URL Error')
                        return
                result = result or clauseResult

                if clauseResult:
                    if len(condition_met_string) >= 1:
                        clause_met.append(condition_met_string[:-1])

            if result:
                # if it is active sound alarm
                if active == 1:
                    now = datetime.now()
                    dt_string = now.strftime('%d/%m/%Y')
                    tm_string = now.strftime('%H:%M:%S')
                    print(dt_string, ', ', tm_string, ': ', self.triggerId, 'Alert', sep=' ')
                    if self.trigger.trigger_activation_time == 'No':
                        self.trigger.trigger_activation_time = tm_string
                    if self.trigger.trigger_activation_date == 'No':
                        self.trigger.trigger_activation_date = dt_string

                    self.serverIO.pushNotification(self.trigger, clause_met)
                    self.need_to_change_status = True
                    # active = 0
            else:
                # if not active switch back to active
                if active == 0 and self.need_to_change_status is True:
                    self.serverIO.setBackToActive(self.triggerId)
                    self.need_to_change_status = False
                print(self.triggerId, 'Passed', sep=' ')
            time.sleep(self.interval)

    def __init__(self, trigger):
        self.conditionMet = False
        self.serverIO = ServerIO()
        self.need_to_change_status = False

        if trigger is not None:
            self.trigger = trigger
            self.refresh_time = 60
            self.triggerId = trigger.trigger_id
            self.src = trigger.src
            self.conditions = trigger.condition
            self.trigger_owner = trigger.owner
            self.interval = trigger.interval 
            self.port = trigger.port

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

                reg = re.match(r'(>=|<=|==|!=|<|=|>|contains|does not contain)(-?[0-9]+)', cond)
                if reg is not None:
                    clause = reg.group(1)
                    if clause == 'contains' and clause == 'does not contain':
                        val = clause.lower()
                    else:
                        val = float(reg.group(2))

                    if clause is not None and val is not None:
                        if clause == "==" or clause == "=" or clause == 'contains':
                            cmpFun = self.equal_equal
                        elif clause == ">=":
                            cmpFun = self.greater_equal
                        elif clause == "<=":
                            cmpFun = self.lesser_equal
                        elif clause == ">":
                            cmpFun = self.greater
                        elif clause == "<":
                            cmpFun = self.lesser
                        elif clause == '!=' or clause == 'does not contain':
                            cmpFun = self.not_equal

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
    def not_equal(a, b):
        return a != b

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

# PUBLIC FUNCTIONS
