import array
import math
from random import randint
import time as Time


import simpleaudio as sa

import chanceGrid
import midiParser
import threadingTimer

bpm = 120
beatsPerBar = 8
beatValue = 8

barLength = int((8 / beatValue) * beatsPerBar)

eigthDuration = (60 / bpm) / 2

beatCounter = 0
globalCounter = 0
globalLimit = (barLength * 2) - 1

kick = sa.WaveObject.from_wave_file("samples/kick.wav")
snare = sa.WaveObject.from_wave_file("samples/snare.wav")
hat = sa.WaveObject.from_wave_file("samples/hat.wav")

midi = midiParser.MidiParser(3, bpm);

# kickSequence = [1, 0, 0, 0, 0, 6, 0, 0]
# snareSequence = [0, 0, 3, 0, 0, 0, 7, 0]
# hatSequence = [1, 2, 3, 4, 5, 6, 7, 8]

#sys.stdin.read(1)

kickSequence = []
snareSequence = []
hatSequence = []

for i in range(barLength):
   kickSequence.append(0)
   snareSequence.append(0)
   hatSequence.append(0)




test = chanceGrid.ChanceGrid([1,2,3,4,5,6]);
print(test.generate(5))

def ticker():
   #define as global, otherwise incrementing value will scope it locally
   global beatCounter, globalCounter

   #counts beat in bar
   beatCounter += 1

   #sets limit to thread
   globalCounter += 1

   #scan sequence arrays each beat
   for i in range(0, barLength):
      if beatCounter == kickSequence[i]:
         kick.play()
      if beatCounter == snareSequence[i]:
         snare.play()
      if beatCounter == hatSequence[i]:
         hat.play()

   #reset beat counter
   if beatCounter > barLength - 1:
      beatCounter = 0

   #stop timer after global count limit
   if globalCounter > globalLimit:
      timer.cancel()

   print("tick")

def generateMidiFile():
   #parameters: track, pitch, time, duration
   midi.addNote(0, 60, 0, 0.5)
   midi.addNote(0, 60, 1, 0.5)
   midi.addNote(0, 60, 2, 0.5)
   midi.addNote(0, 60, 3, 0.5)
   midi.exportFile("test.mid")

timer = threadingTimer.ThreadingTimer(eigthDuration,ticker)
timer.start()

# print("Please enter your name and hit enter.")
# userName = input("Your name = ")