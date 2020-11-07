import threading
import ServerIO
from Monitor import Monitor
import UpdateMonitors

url = ''

api_url = '127.0.0.1'
api_user = 'root'
api_pwd = '63MH0UT7DCW30'

defined_monitors = {}


# Code below is used to send relation's output to the server
# @todo
# output_json = relation.outputSource.make_json()
# ServerIO.send_server_request(url, output_json)


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
                monitor = defined_monitors['WebsiteHealthMonitor']
                monitor_thread = threading.Thread(target=monitor.run())
                self.monitors.append(monitor_thread)

    def start_monitors(self):
        for monitor in self.monitors:
            monitor.start()

    def wait_join(self):
        for monitors in self.monitors:
            monitors.join()


def __main__():
    global defined_monitors
    orchestrator = Orchestrator()
    UpdateMonitors.__main__()
    defined_monitors = UpdateMonitors.monitors
    orchestrator.initialize_monitors()
    orchestrator.start_monitors()
    orchestrator.wait_join()


__main__()
