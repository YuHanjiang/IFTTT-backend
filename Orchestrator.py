import threading
import ServerIO
import UpdateMonitors 
import time

url = ''

api_url = '127.0.0.1'
api_user = 'root'
# api_pwd = ''
api_pwd = '63MH0UT7DCW30'

defined_monitors = {}


class Orchestrator:
    def __init__(self):
        self.triggers = []  # collection of threads that will run checker functions
        self.monitors = []
        self.triggerIds = set([])
    def add_triggers(self): 
        #add new triggers to current triggers in the system
        newTriggers = ServerIO.read_triggers(api_url, api_user, api_pwd, self.triggerIds)  
        self.triggers.extend(newTriggers)
        for trigger in self.triggers: 
            self.triggerIds.add(trigger.trigger_id)

    # create and start threads for each each relation with appropriate checker function 
    def initialize_monitors(self):
        # will later fix so new monitors don't have to be hard coded in
        for trigger in self.triggers: 
            if trigger.hasMonitor == False: 
                trigger.hasMonitor = True
                if trigger.monitor == 'Website Health Check':
                    monitor = defined_monitors['WebsiteHealthMonitor']
                    monitor_thread = threading.Thread(target=monitor.start, args=(trigger,)) 
                    monitor_thread.start()
                    self.monitors.append(monitor_thread)



    def update(self):   
        while True:
            time.sleep(10)   
            self.add_triggers() 
            self.initialize_monitors()




def __main__():
    global defined_monitors
    orchestrator = Orchestrator()
    orchestrator.add_triggers()
    UpdateMonitors.__main__()
    defined_monitors = UpdateMonitors.monitors
    orchestrator.initialize_monitors()
    orchestrator.update()


__main__()
