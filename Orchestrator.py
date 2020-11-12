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
        self.monitors = {}
        self.triggerIds = set([])

    def update_triggers(self):
        # add new triggers to current triggers in the system
        (newTriggers, remove_triggers) = ServerIO.read_triggers(api_url, api_user, api_pwd, self.triggerIds)
        self.triggers.extend(newTriggers)
        for trigger in self.triggers:
            self.triggerIds.add(trigger.trigger_id)
        to_remove = []
        for trigger in self.triggers:
            if trigger.trigger_id in remove_triggers:
                trigger.terminated = True
                to_remove.append(trigger)

        for t in to_remove:
            self.triggers.remove(t)

        for rm_t in remove_triggers:
            self.monitors[rm_t] = None

    # create and start threads for each each relation with appropriate checker function
    def initialize_monitors(self):
        # will later fix so new monitors don't have to be hard coded in
        for trigger in self.triggers:
            if not trigger.hasMonitor:
                trigger.hasMonitor = True
                if trigger.monitor == 'Website Health Check':
                    monitor = defined_monitors['WebsiteHealthMonitor']
                    monitor_thread = threading.Thread(target=monitor.start, args=(trigger,))
                    monitor_thread.start()
                    self.monitors[trigger.trigger_id] = monitor_thread

    def update(self):
        while True:
            self.update_triggers()
            self.initialize_monitors()
            time.sleep(10)


def __main__():
    global defined_monitors
    orchestrator = Orchestrator()
    UpdateMonitors.update_monitors()
    defined_monitors = UpdateMonitors.monitors
    orchestrator.initialize_monitors()
    orchestrator.update()


__main__()
