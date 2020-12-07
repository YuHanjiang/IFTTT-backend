from Monitor import Monitor
import MonitorVarTypes
import requests

monitor_var = {'Previous Closing Price': MonitorVarTypes.FLOAT}


class PolygonStockAPIMonitor(Monitor):

    def _mapper(self):
        return {'Previous Closing Price': self._price_check}

    def _price_check(self, func, val):
        try:
            r = requests.get(self.src)
            if r.status_code == 200:
                stock_json = r.json()
                closing_price = stock_json['results'][0]['c']
                return func(closing_price, val)

        except Exception as err:
            raise ValueError


def start(trigger):
    monitor = PolygonStockAPIMonitor(trigger)
    monitor.run()

