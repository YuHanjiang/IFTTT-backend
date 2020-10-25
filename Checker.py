import requests, pythonping, re, time


# abstract Checker class to be implemented in the backend of IFTTT
class Checker:

    # Initialize Checker object and input the trigger
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
        self.map = {}


    
       
    def mapper(self): 
        pass 

    def _dicParsaer(self):   
              

            for key in self.conditions.keys(): 
                self.funcList.append(self.map[key]) 

            for string in self.conditions.values():  
                reg = re.match("([<>=][<>=])([0-9]*|[0-9]*.[0.9]*)", string)
                clause = reg.group(1)
                val = float(reg.group(2))

                if clause == "==":
                    cmpFun = self.equalequal
                elif clause == ">=":
                    cmpFun = self.greaterequal
                elif clause == "<=":
                    cmpFun = self.lesserequal
                
                self.paraList.append((cmpFun, val)) 
    

    # Start the checker and check what is the method of checking
    # The method returns true if the check satisfies the user's defined condition 

   

    @staticmethod
    def equalequal(a, b):
        if a == b:
            return True
        else:
            return False

    @staticmethod
    def greaterequal(a, b):
        if a >= b:
            return True
        else:
            return False

    @staticmethod
    def lesserequal(a, b):
        if a <= b:
            return True
        else:
            return False


##***PUBLIC FUNCTIONS***##
def run(self):

        
        self._dicParsaer(self);  

        while(True): 

            for i in range(len(self.funcList)): 
                if self.funcList[i](self.paraList[i][0],self.paraList[i][1]) == True: 
                    self.conditionMet = True 
                    break

            time.sleep(self.interval) 