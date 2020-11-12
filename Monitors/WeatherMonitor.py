from Monitor import Monitor
import json
import requests

monitor_var = ["Temp"]


class WeatherMonitor(Monitor):

    def _mapper(self):
        varToFuncMapping = {'Temp': self._temp_check}

        return varToFuncMapping

    def _temp_check(self, func, val):
        try:
            r = requests.get("http://" + self.src)
            if r.status_code == 200:
                temp = float(json.loads(r.json())["main"]["temp"])
                return func(temp, val)
            else:
                return True

        except requests.exceptions.RequestException as err:
            print('Access Denied')
            return True


def start(trigger):
    monitor = WeatherMonitor(trigger)
    monitor.run()
