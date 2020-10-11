import requests, pythonping, re, time


# Checker class to be implemented in the backend of IFTTT
class Checker:

    # Initialize Checker object and input the trigger
    def __init__(self, relation):
        if relation is not None:
            self.trigger = relation.trigger
            self.relation = relation
            self.url = self.trigger.src
            self.method = self.trigger.method
            self.val = 0  
            self.cmpFun = None 
            self.interval = self.trigger.interval

    
    def conditionParser(self):  
         
        reg = re.match("([<>=][<>=])([0-9]*|[0-9]*.[0.9]*)",self.trigger.condition) 
        clause = reg.group(1) 
        self.val = float(reg.group(2))

        if clause == "==": 
            self.cmpFun = self.equalequal 
        elif clause == ">=": 
            self.cmpFun = self.greaterequal 
        elif clause == "<=": 
            self.cmpFun = self.lesserequal


    # Start the checker and check what is the method of checking
    # The method returns true if the check satisfies the user's defined condition
    def start(self): 
        
        self.conditionParser() 

        if self.method == 'PING':
            while not self.relation.isPulled:
                if self.ping_request(self.url, self.cmpFun, self.val):
                    self.relation.isPulled = True 
                time.sleep(self.interval)

        elif self.method == 'HTTPRESP':
            while not self.relation.isPulled:
                if self.http_request(self.url):
                    self.relation.isPulled = True 
                time.sleep(self.interval) 

    # Ping a website and return whether the response time is smaller than the given value
    @staticmethod
    def ping_request(url,cmpFun,val):
        r = pythonping.ping(url, size=50)

        return cmpFun(a=r.rtt_avg_ms, b= val)

    # Send a http request to the given site and returns whether the site is reachable
    @staticmethod
    def http_request(url): 
        try:
            r = requests.get(url) 
        except requests.exceptions.RequestException as err: 
            return True

        return r.status_code is not requests.codes.ok 

    @staticmethod
    def equalequal(a,b): 
        if a == b: 
            return True 
        else: 
            return False 

    @staticmethod
    def greaterequal(a,b): 
        if a >= b: 
            return True 
        else: 
            return False 

    @staticmethod
    def lesserequal(a,b): 
        if a <= b: 
            return True 
        else: 
            return False
