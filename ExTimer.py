#-*- coding: utf-8 -*-

from threading import Timer,Thread,Event

# Usage :
# variable = ExTimer(time_value(second), Handler Function)
# variable.start()
# Stopped timer -> t.cance()
# t = ExTimer(3,printer)
#t2 = ExTimer(1,printer2)
#t.start()
#t2.start()

class ExTimer():
 
    def __init__(self,t,hFunction):
        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t,self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t,self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

