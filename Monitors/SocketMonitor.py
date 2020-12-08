from Monitor import Monitor 
import MonitorVarTypes
import socket  

monitor_var = {"Connection": MonitorVarTypes.INT}  
monitor_text = "URL FORMAT: www.{WEBSITE.com}; \nPort Number also required."

class SocketMonitor(Monitor):  

    def _mapper(self):
        varToFuncMapping = {'Connection': self._connection_check}

        return varToFuncMapping 

    def _connection_check(self, func, val): 
        address = (self.src,self.port )      
        suc =0
        try:
            socket.create_connection(address=address) 
            suc = 1  
        except:  
            suc = 0 

        return func(suc,val)

def start(trigger):
    monitor = SocketMonitor(trigger)
    monitor.run()