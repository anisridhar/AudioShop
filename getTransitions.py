#getting transitions between notes

from pydub import AudioSegment
from pydubtest import play, make_chunks

song = AudioSegment.from_wav("noteTransitions.wav")[:2000]
song = AudioSegment.from_wav("Notes/da.wav")[1000:]
play(song)
#song.export("Notes/highSa.wav",format="wav")
song.export("Notes/da.wav",format="wav")
