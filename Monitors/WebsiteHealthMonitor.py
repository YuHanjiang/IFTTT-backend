import requests
import pythonping
from Monitor import Monitor

monitor_var = ['StatusCode', 'Latency']


class WebsiteHealthChecker(Monitor):

    def _mapper(self):
        varToFuncMapping = {'StatusCode': self._HTTPRESP_check, 'Latency': self._ping_check}

        return varToFuncMapping

    def _HTTPRESP_check(self, func, val):
        try:
            r = requests.get('http://' + self.src)

        except requests.exceptions.RequestException as err:
            print(self.src)
            print('Access Denied')
            return True

        return func(int(r.status_code), val)

    def _ping_check(self, func, val):
        r = pythonping.ping(self.src, size=50)
        a = r.rtt_avg_ms
        return func(float(a), val)


def start(trigger):
    monitor = WebsiteHealthChecker(trigger)
    monitor.run()
