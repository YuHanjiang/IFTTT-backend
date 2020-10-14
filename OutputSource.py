import json


class OutputSource:

    def __init__(self, text, key, severity, audience):
        self.text = text
        self.key = key
        self.severity = severity
        self.audience = audience

    def make_json(self):
        output_json = {
            'text': self.text,
            'key': self.key,
            'severity': self.severity,
            'audience': self.audience
        }

        return json.dumps(output_json)
