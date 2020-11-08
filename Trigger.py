class Trigger:

    def __init__(self, trigger_id, src, monitor, condition, severity, owner):
        self.trigger_id = trigger_id
        self.src = src
        self.condition = condition
        self.severity = severity
        self.monitor = monitor
        self.owner = owner

