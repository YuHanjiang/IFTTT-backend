class Trigger:

    def __init__(self, src, checker, conditions, interval, id, text):
        self.src = src
        self.checker =  checker
        self.conditions = conditions
        self.interval = interval  
        self.id = id
        self.text = text
