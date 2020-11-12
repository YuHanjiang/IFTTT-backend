class Trigger:

    def __init__(self, trigger_id, src, monitor, condition, severity, owner, condition_string):
        self.trigger_id = trigger_id
        self.src = src
        self.condition = condition
        self.severity = severity
        self.monitor = monitor
        self.owner = owner
        self.condition_string = condition_string 
        self.hasMonitor = False
        self.terminated = False
