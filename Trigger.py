class Trigger:

    def __init__(self, src, monitor, condition, severity):
        self.src = src
        self.condition = condition
        self.severity = severity
        self.monitor = monitor
