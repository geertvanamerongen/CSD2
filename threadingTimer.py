from threading import Timer,Thread,Event

threadingFlag = True

class ThreadingTimer():
   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handleFunction)

   def handleFunction(self):
      if threadingFlag:
         self.hFunction()
         self.thread = Timer(self.t,self.handleFunction)
         self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      global threadingFlag
      self.thread.cancel()
      threadingFlag = False
      print("threading timer stopped")