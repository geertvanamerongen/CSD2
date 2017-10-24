import array
from random import randint

class ChanceGrid:
   def __init__(self, arr):
      self.stepArr = []
      self.chanceArr = []
      
      #init chance array with even chances
      for i in range(len(arr)):
         self.stepArr.append(arr[i])
         self.chanceArr.append(round(100 / len(arr)))

      #make sure total chance is 100%
      # print("stepArr: "+str(self.stepArr))
      # print("chanceArr: "+str(self.chanceArr))
      self._roundToHundred()

   def getSteps(self):
   	  return self.stepArr

   def getChances(self):
   	  return self.chanceArr

   def updateChance(self, step, multiplier):
      #step index
      s = None

      #determine step index
      for i in range(len(self.stepArr)):
         if self.stepArr[i] == step:
            s = i
            break

      if s != None:
         #determine difference when multiplier is 0
         if multiplier == 0:
            delta = -(self.chanceArr[s])

         else:
            #calculate difference
            delta = round((self.chanceArr[s] * multiplier) - self.chanceArr[s])

            #apply ceiling limit to difference
            if self.chanceArr[s] + delta > 100:
               delta = 100 - self.chanceArr[s]
            #apply floor limit to difference
            elif self.chanceArr[s] + delta < 0:
               delta = -(self.chanceArr[s])

            #add difference to step
            self.chanceArr[s] += delta

         #distribute negative difference amongst remaining steps
         for i in range(len(self.stepArr)):
            if s != i:
               self.chanceArr[i] += round(-(delta / (len(self.chanceArr) - 1)))
               if self.chanceArr[i] < 0:
                  self.chanceArr[i] = 0

         #delete step when multiplier is 0
         if multiplier == 0:
            self.chanceArr.pop(s)
            self.stepArr.pop(s)

         #make sure total chance is 100%
         self._roundToHundred()
      else:
         print("Step not found!")

   def generate(self, amount):
      result = []
      
      for i in range(amount):
         step = self._pickRandomStep()
         while step in result:
            step = self._pickRandomStep()
         result.append(step)

      return result

   def _roundToHundred(self, exclude=-1):
      l = len(self.stepArr) - 1
      while self._getTotal() < 100:
         r = randint(0, l)
         while self.chanceArr[r] >= 100:
            r = randint(0, l)
         self.chanceArr[r] += 1
      while self._getTotal() > 100:
         r = randint(0, l)
         while self.chanceArr[r] <= 0:
            r = randint(0, l)
         self.chanceArr[r] -= 1

   def _getTotal(self):
      total = 0
      for i in range(len(self.chanceArr)):
         total += self.chanceArr[i]
      return total

   def _pickRandomStep(self):
      chanceRange = []
      count = 0
      rand = randint(0,99)

      for i in range(len(self.chanceArr)):
         count += self.chanceArr[i]
         chanceRange.append(count)

      for i in range(len(chanceRange)):
         if(rand < chanceRange[i]):
            return self.stepArr[i]