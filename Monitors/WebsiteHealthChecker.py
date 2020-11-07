import requests
from Monitor import Monitor


class WebsiteHealthChecker(Monitor):

    def _mapper(self):
        varToFuncMapping = {'Status Code': self._HTTPRESP_check}
        return varToFuncMapping

    def _HTTPRESP_check(self, func, val):
        try:
            r = requests.get(self.src)

        except requests.exceptions.RequestException as err:
            print(err)
            return True

        return func(float(r.status_code), val)


def run(trigger):
    monitor = WebsiteHealthChecker(trigger)
    monitor.run()
