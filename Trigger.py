class Trigger:

    def __init__(self, trigger_id, src, monitor, condition, severity, owner, condition_string, interval, port, message):
        self.trigger_id = trigger_id
        self.src = src
        self.trigger_activation_date = "No"
        self.trigger_activation_time = "No"
        self.condition = condition
        self.severity = severity
        self.monitor = monitor
        self.owner = owner
        self.condition_string = condition_string
        self.interval = interval
        self.port = port
        self.hasMonitor = False
        self.terminated = False
        self.message = message
