import threading
import ServerIO
from Monitor import Monitor
import UpdateMonitors

url = ''

api_url = '127.0.0.1'
api_user = 'root'
api_pwd = ''
# api_pwd = '63MH0UT7DCW30'

defined_monitors = {}


class Orchestrator:
    def __init__(self):
        self.triggers = []  # collection of threads that will run checker functions
        self.monitors = []

    def add_triggers(self):
        self.triggers = ServerIO.read_triggers(api_url, api_user, api_pwd)

    # create and start threads for each each relation with appropriate checker function
    def initialize_monitors(self):
        for trigger in self.triggers:
            if trigger.monitor == 'Website Health Check':
                monitor = defined_monitors['WebsiteHealthChecker']
                monitor_thread = threading.Thread(target=monitor.run(trigger))
                self.monitors.append(monitor_thread)

    def start_monitors(self):
        for monitor in self.monitors:
            monitor.start()

        for monitors in self.monitors:
            monitors.join()


def __main__():
    global defined_monitors
    orchestrator = Orchestrator()
    orchestrator.add_triggers()
    UpdateMonitors.__main__()
    defined_monitors = UpdateMonitors.monitors
    orchestrator.initialize_monitors()
    orchestrator.start_monitors()


__main__()
