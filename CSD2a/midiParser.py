from midiutil.MidiFile import MIDIFile

class MidiParser:
	def __init__(self, numberOfTracks, tempo, volume=100, channel=0):
		self.numberOfTracks = numberOfTracks
		self.tempo = tempo
		self.volume = volume
		self.channel = channel

		self.midiFile = MIDIFile(numberOfTracks)

		for i in range(self.numberOfTracks - 1):
			self.midiFile.addTrackName(i, 0, "Track " + str(i + 1))
			self.midiFile.addTempo(i, 0, self.tempo)

	def addNote(self, track, pitch, time, duration):
		self.midiFile.addNote(track, self.channel, pitch, time, duration, self.volume)

	def exportFile(self, filename):
		with open(filename, 'wb') as exportFile:
			self.midiFile.writeFile(exportFile)