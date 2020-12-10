from Monitor import Monitor
import MonitorVarTypes
import requests

monitor_var = {'PreviousClosingPrice': MonitorVarTypes.FLOAT} 
monitor_text = "URL FORMAT: https://api.polygon.io/v2/aggs/ticker/{TICKER}/prev?apiKey={APIKEY}; \nGo to https://polygon.io/docs/get_v1_meta_symbols__stocksTicker__news_anchor for more info"


class PolygonStockAPIMonitor(Monitor):

    def _mapper(self):
        return {'PreviousClosingPrice': self._price_check}

    def _price_check(self, func, val):
        try:
            r = requests.get(self.src)
            if r.status_code == 200:
                stock_json = r.json()
                closing_price = stock_json['results'][0]['c']
                return func(closing_price, val), closing_price

        except Exception:
            raise ValueError


def start(trigger):
    monitor = PolygonStockAPIMonitor(trigger)
    monitor.run()

