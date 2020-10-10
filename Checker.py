import requests, pythonping


# Checker class to be implemented in the backend of IFTTT
class Checker:

    # Initialize Checker object and input the trigger
    def __init__(self, relation):
        if relation is not None:
            self.trigger = relation.trigger
            self.relation = relation
            self.url = self.trigger.src
            self.method = self.trigger.method
            self.val = self.trigger.condition

    # Start the checker and check what is the method of checking
    # The method returns true if the check satisfies the user's defined condition
    def start(self):
        if self.method is 'ping':
            while not self.relation.isPulled:
                if not self.ping_request(self.url, self.val):
                    self.relation.isPulled = True

        elif self.method is 'http':
            while not self.relation.isPulled:
                if not self.http_request(self.url):
                    self.relation.isPulled = True

    # Ping a website and return whether the response time is smaller than the given value
    @staticmethod
    def ping_request(url, val):
        r = pythonping.ping(url, size=50)

        return r.rtt_avg_ms < val

    # Send a http request to the given site and returns whether the site is reachable
    @staticmethod
    def http_request(url):
        r = requests.get(url)

        return r.status_code is requests.codes.ok
