from threading import Timer,Thread,Event

class ThreadingTimer():
   def __init__(self,t,hFunction):
      self.t = t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handleFunction)
      self.threadingFlag = True

   def handleFunction(self):
      if self.threadingFlag:
         self.hFunction()
         self.thread = Timer(self.t,self.handleFunction)
         self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()
      self.threadingFlag = False