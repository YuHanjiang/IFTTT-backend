import requests
import pythonping
from Monitor import Monitor
import MonitorVarTypes

monitor_var = {'StatusCode': MonitorVarTypes.INT, 'Latency': MonitorVarTypes.FLOAT}


class WebsiteHealthChecker(Monitor):

    def _mapper(self):
        varToFuncMapping = {'StatusCode': self._HTTPRESP_check, 'Latency': self._ping_check}

        return varToFuncMapping

    def _HTTPRESP_check(self, func, val):
        try:
            r = requests.get('http://' + self.src)

        except Exception as err:
            print(self.src)
            print('Access Denied:', self.triggerId, sep=' ')
            return True

        return func(int(r.status_code), val)

    def _ping_check(self, func, val):
        try:
            r = pythonping.ping(self.src, size=50)
            a = r.rtt_avg_ms
            return func(float(a), val)
        except Exception as err:
            return True


def start(trigger):
    monitor = WebsiteHealthChecker(trigger)
    monitor.run()
