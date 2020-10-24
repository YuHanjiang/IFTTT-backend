import pythonping 
import requests
from Checker import Checker 

class WebsiteHealthChecker(Checker): 
     
    def _mapper(self):  
        varToFuncMapping = {}       
        varToFuncMapping["PING"] = self._ping_check 
        varToFuncMapping["HTTPRESP"] = self._HTTPRESP_check 
        return varToFuncMapping

    def _ping_check(self, func, val): 
        r = pythonping.ping(self.src, size=50)
        a=r.rtt_avg_ms 
        return func(a,val)  

    def _HTTPRESP_check(self,func,val): 
        try:
            r = requests.get(self.src) 
        except requests.exceptions.RequestException as err: 
            return True

        return func(r.status_code,val) 
    