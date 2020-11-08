import requests
import pythonping
from Monitor import Monitor

monitor_var = ['Status Code', 'Latency']


class WebsiteHealthChecker(Monitor):

    def _mapper(self):
        varToFuncMapping = {'Status Code': self._HTTPRESP_check, 'Latency': self._ping_check}

        return varToFuncMapping

    def _HTTPRESP_check(self, func, val):
        try:
            r = requests.get(self.src)
            print(r.status_code)
        except requests.exceptions.RequestException as err:
            print(err)
            return True

        return func(float(r.status_code), val)

    def _ping_check(self, func, val):
        r = pythonping.ping(self.src, size=50)
        a = r.rtt_avg_ms
        print(a)
        return func(float(a), val)


def run(trigger):
    monitor = WebsiteHealthChecker(trigger)
    monitor.run()
