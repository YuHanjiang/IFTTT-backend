from Monitor import Monitor
import requests

monitor_var = ["Temp", "Weather"]


class WeatherMonitor(Monitor):

    def _mapper(self):
        varToFuncMapping = {'Temp': self._temp_check, 'Weather':self._weather_check}

        return varToFuncMapping

    def _temp_check(self, func, val):
        try:
            r = requests.get("http://" + self.src)
            if r.status_code == 200:
                try:
                    weather_json = r.json()
                    temp = float(weather_json['main']['temp'])
                    return func(temp, val)
                except KeyError as ke:
                    print("No key:", ke, sep=' ')
                    return True
            else:
                return True

        except requests.exceptions.RequestException as err:
            print('Access Denied')
            return True

    def _weather_check(self, func, val):
        try:
            r = requests.get("http://" + self.src)
            if r.status_code == 200:
                try:
                    weather_json = r.json()
                    temp = weather_json['weather'][0]['main'].lower()
                    return func(temp, val)
                except KeyError as ke:
                    print("No key:", ke, sep=' ')
                    return True
            else:
                return True

        except requests.exceptions.RequestException as err:
            print('Access Denied')
            return True


def start(trigger):
    monitor = WeatherMonitor(trigger)
    monitor.run()
