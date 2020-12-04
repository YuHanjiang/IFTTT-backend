from Monitor import Monitor
import MonitorVarTypes
import requests

monitor_var = {"Temp": MonitorVarTypes.FLOAT, "Humidity": MonitorVarTypes.FLOAT}


class WeatherMonitor(Monitor):

    def _mapper(self):
        varToFuncMapping = {'Temp': self._temp_check, 'Humidity': self._humidity_check}

        return varToFuncMapping

    def _temp_check(self, func, val):
        try:
            r = requests.get("http://" + self.src)
            if r.status_code == 200:
                weather_json = r.json()
                if 'main' in weather_json and 'temp' in weather_json['main']:
                    temp = float(weather_json['main']['temp'])
                    return func(temp, val)
        except requests.exceptions.RequestException as err:
            self.trigger.terminated = True
            return True

    def _humidity_check(self, func, val):
        try:
            r = requests.get("http://" + self.src)
            if r.status_code == 200:
                weather_json = r.json()
                if 'main' in weather_json and 'humidity' in weather_json['main']:
                    hum = weather_json['main']['humidity']
                    return func(hum, val)

        except requests.exceptions.RequestException as err:
            self.trigger.terminated = True
            return True

        except KeyError as key_err:
            print('Json Key Error: ', self.triggerId)
            return True


def start(trigger):
    monitor = WeatherMonitor(trigger)
    monitor.run()
