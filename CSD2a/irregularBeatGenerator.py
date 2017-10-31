import array
import math
from random import randint
import time as Time

import simpleaudio as sa

import chanceGrid
import midiParser
import threadingTimer

bpm = 0
beatsPerBar = 0
beatValue = 0

allowedBeatValues = [2,4,8,16]

gridLength = 0
stepDuration = 0

beatCounter = 0

kick = sa.WaveObject.from_wave_file("samples/kick.wav")
snare = sa.WaveObject.from_wave_file("samples/snare.wav")
hat = sa.WaveObject.from_wave_file("samples/hat.wav")

isPaused = False

kickSequence = []
snareSequence = []
hatSequence = []

beatTimerArr = []

def inputBpm():
   global bpm, stepDuration

   while bpm < 1:
      userInput = input("Enter BPM: ")
      try:
         bpm = int(userInput)
         if bpm < 1:
            print("Error - enter a whole number above 0")
      except ValueError:
         print("Error - enter a whole number above 0")
   stepDuration = (60 / bpm) / 4


def inputBeatsPerBar():
   global beatsPerBar

   while beatsPerBar < 1:
      userInput = input("Enter number of beats per bar: ")
      try:
         beatsPerBar = int(userInput)
         if beatsPerBar < 1:
            print("Error - enter a whole number above 0")
      except ValueError:
         print("Error - enter a whole number above 0")

def inputBeatValue():
   global beatValue
   global allowedBeatValues

   while (beatValue in allowedBeatValues) == False:
      userInput = input("Enter beat value: ")
      try:
         beatValue = int(userInput)
         if (beatValue in allowedBeatValues) == False:
            print("Error - allowed values: "+str(allowedBeatValues))
      except ValueError:
         print("Error - allowed values: "+str(allowedBeatValues))


def createBeat():
   #create full grid as start array for different voices
   global kickSequence, snareSequence, hatSequence, gridLength

   gridLength = int((16 / beatValue) * beatsPerBar)

   kickSequence = []
   snareSequence = []
   hatSequence = []

   fullGrid = []
   for i in range(gridLength):
      fullGrid.append(i + 1)

   #determine amount of hits for each voice
   kickAmount = randint(math.ceil(gridLength / 8), math.ceil(gridLength / 3))
   snareAmount = randint(1, math.ceil(gridLength / 4))
   hatAmount = randint(math.ceil(gridLength / 4), gridLength - 1)
   
   #KICK
   kickGrid = chanceGrid.ChanceGrid(fullGrid)
   
   for i in range(len(kickGrid.getSteps())):
      #if step is first beat in bar, increase change by 5
      if (kickGrid.getSteps()[i] % 4) == 1:
         kickGrid.updateChance(kickGrid.getSteps()[i], 5)

      #if step is first beat in bar, increase change by 2.5
      if (kickGrid.getSteps()[i] % 4) == 3:
         kickGrid.updateChance(kickGrid.getSteps()[i], 2.5)
  
  #pick cycle
   while(len(kickSequence) < kickAmount):
      x = kickGrid.generate(1)[0]
      kickGrid.updateChance(x, 0)
      kickSequence.append(x)

      arr = kickGrid.getSteps()
      for i in range(len(arr)):
         #check if step is in same 4 step window and if so, decrease chance of being picked
         if math.ceil(x/4) == math.ceil(arr[i]/4):
            kickGrid.updateChance(arr[i], 0.1)

   #SNARE
   snareGrid = chanceGrid.ChanceGrid(fullGrid)

   for i in range(len(snareGrid.getSteps())):
      if (snareGrid.getSteps()[i] in kickSequence):
         #decrease chance when sharing step with kick
         snareGrid.updateChance(snareGrid.getSteps()[i], 0.2)

   
   #pick cycle
   while(len(snareSequence) < snareAmount):
      x = snareGrid.generate(1)[0]
      snareGrid.updateChance(x, 0)
      snareSequence.append(x)

      snareArr = snareGrid.getSteps()
      for i in range(len(snareArr)):
         #check if step is in same 4 step window and if so, decrease chance of being picked
         if math.ceil(x/4) == math.ceil(snareArr[i]/4):
            snareGrid.updateChance(snareArr[i], 0.1)

   #HATS
   hatGrid = chanceGrid.ChanceGrid(fullGrid)


   for i in range(len(hatGrid.getSteps())):
      if (hatGrid.getSteps()[i] in snareSequence):
         #decrease chance when sharing step with snare
         hatGrid.updateChance(hatGrid.getSteps()[i], 0.2)

      if (hatGrid.getSteps()[i] in kickSequence):
         #decrease chance when sharing step with kick
         hatGrid.updateChance(hatGrid.getSteps()[i], 0.2)

      if (hatGrid.getSteps()[i] % 2) == 0:
         hatGrid.updateChance(hatGrid.getSteps()[i], 2)

      if (hatGrid.getSteps()[i] % 4) == 3:
         hatGrid.updateChance(hatGrid.getSteps()[i], 2)

   #pick cycle
   while(len(hatSequence) < hatAmount):
      y = hatGrid.generate(1)[0]
      hatGrid.updateChance(y, 0)
      hatSequence.append(y)

      hatArr = hatGrid.getSteps()
      for i in range(len(hatArr)):
         #check if step is in same 4 step window and if so, decrease chance of being picked
         if math.ceil(y/4) == math.ceil(hatArr[i]/4):
            hatGrid.updateChance(hatArr[i], 0.1)

def inputHandler():
   global isPaused, beatCounter, bpm, beatsPerBar, beatValue
   
   commands = ["play", "pause", "stop", "bpm", "beatsPerBar", "beatValue", "export", "generate", "commands", "close"]

   command = input()

   if(command in commands):
      #play
      if command == commands[0]:
         isPaused = False
         print("Playing track from beat: " + str(beatCounter))

      #pause
      if command == commands[1]:
         print("Paused track at beat: " + str(beatCounter))
         isPaused = True

      #stop
      if command == commands[2]:
         isPaused = True
         beatCounter = 1
         print("Track stopped")

      #bpm
      if command == commands[3]:
         bpm = 0
         inputBpm()
         startNewBeatTimer()
         print("BPM changed to "+str(bpm))

      #beatsPerBar
      if command == commands[4]:
         beatsPerBar = 0
         inputBeatsPerBar()
         print("Beats per bar changed to: "+str(beatsPerBar) + " (applied when generating new beat)")

      #beatValue
      if command == commands[5]:
         beatValue = 0
         inputBeatValue()
         print("Beat value changed to: "+str(beatValue) + " (applied when generating new beat)")

      #export
      if command == commands[6]:
         command = input("Enter name: ")
         generateMidiFile(command)

      #generate
      if command == commands[7]:
         createBeat()
         print("Generating new beat")

      #commands
      if command == commands[8]:
         print(str(commands))
      
      #close
      if command == commands[9]:
         beatTimerArr[len(beatTimerArr) - 1].cancel()
         inputTimer.cancel()
   else:
      print("Error - command unknown. Allowed commands: " + str(commands))

def ticker():
   #define as global, otherwise incrementing value will scope it locally
   global beatCounter
   #check is paused
   if isPaused == False:
      
      #counts beat in bar
      beatCounter += 1

      #check if voices need to play on each beat
      if beatCounter in kickSequence:
         kick.play()

      if beatCounter in snareSequence:
         snare.play()

      if beatCounter in hatSequence:
         hat.play()

      #reset beat counter
      if beatCounter > gridLength - 1:
         beatCounter = 0

def startNewBeatTimer():
   if len(beatTimerArr) == 0:
      beatTimerArr.append(threadingTimer.ThreadingTimer(stepDuration,ticker))
      beatTimerArr[0].start()
   else:
      beatTimerArr.append(threadingTimer.ThreadingTimer(stepDuration,ticker))
      beatTimerArr[len(beatTimerArr) - 2].cancel()
      beatTimerArr[len(beatTimerArr) - 1].start()


def generateMidiFile(name):
   midi = midiParser.MidiParser(3, bpm);

   filename = str(name)+".mid"

   for i in range(len(kickSequence)):
      #parameters: track, pitch, time, duration
      midi.addNote(0, 60, (kickSequence[i] - 1) * 0.5, 0.5)

   for i in range(len(snareSequence)):
      midi.addNote(0, 61, (snareSequence[i] - 1) * 0.5, 0.5)

   for i in range(len(hatSequence)):
      midi.addNote(0, 62, (hatSequence[i] - 1) * 0.5, 0.5)

   midi.exportFile("_export/"+filename)
   print("Exported to: " + filename)

#initial user input
inputBpm()
inputBeatsPerBar()
inputBeatValue()

print("Generating beat")
# run program
createBeat()
startNewBeatTimer()

inputTimer = threadingTimer.ThreadingTimer(stepDuration,inputHandler)
inputTimer.start()

