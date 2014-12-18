import pyaudio
import wave
import sys
import time
import cv2
import numpy as np
import os
from Tkinter import *
from pydubtest import play, make_chunks
from pydub import AudioSegment
from threading import Thread
from vidAnalysis import vid2SoundFile
from eventBasedAnimationClass import EventBasedAnimationClass
import imagesDemo1
from buttonClass import button
from TITLEclass import TITLE
from barePageClass import barePage
from audioEditClass import AUDIOEDIT
from fingerTrackingClass import FINGERTRACKING

class ANALYSIS(barePage):

	#allows user to compare actual recording and denoised

	def __init__(self,width,height):
		super(ANALYSIS,self).__init__(width,height)
		self.started = False

	def initAnalysis(self):
		self.next = None
		self.song = song1 = AudioSegment.from_wav("originalMusic.wav")
		song1 = self.song[1000*self.start:1000*self.end]
		self.song2 = song2 = vid2SoundFile(self.start,self.end,self.fingerData)
		#initializing audio trackBars
		self.bar1 = trackBar(song1,self.width,self.height/3)
		self.bar2 = trackBar(song2,self.width,self.height*2/3)
		#getting new timerDelay
		self.timerDelay = int(round(float(len(song1)/(self.bar1.rightEdge-self.bar1.leftEdge))))

	def draw(self,canvas):
		canvas.create_rectangle(0,0,self.width,self.height,fill="black")
		text1 = "Music from original audio file"
		text2 = "Music from Video Analysis"
		canvas.create_text(self.width/2,self.height/3-50, text = text1,fill="white")
		canvas.create_text(self.width/2,self.height*2/3-50,text=text2,fill="white")
		self.bar1.draw(canvas)
		self.bar2.draw(canvas)

	def onMousePressed(self,event):
		self.bar1.onMousePressed(event)
		self.bar2.onMousePressed(event)

	def onTimerFired(self):
		if self.started:
			self.bar1.onTimerFired()
			self.bar2.onTimerFired()

	def onKeyPressed(self,event):
		self.bar2.onKeyPressed(event)
		if event.keysym == "Right":
			self.song = self.song[:1000*self.start] + self.bar2.song + self.song[1000*self.end:]
			self.next = 1


class trackBar(object):

	#creates a trackbar

	def __init__(self,song,width,cy):
		self.song = song
		self.width = width
		self.cy = cy
		self.leftEdge = self.width/4
		self.rightEdge = 3*self.width/4
		self.trackHeight = 30
		self.lineHeight = self.trackHeight*2
		self.controlWidth = self.trackHeight
		self.control = "play"
		#self.timerDelay = int(round(float(len(self.song)/(self.rightEdge-self.leftEdge))))
		self.trackX = self.leftEdge
		self.recordingStart = 0

	def onMousePressed(self,event):
		if (self.leftEdge-self.controlWidth-5 <= event.x <= self.leftEdge-5 and 
			self.cy-self.trackHeight/2 <= event.y <= self.cy+self.trackHeight/2):
			self.control = "pause" if self.control == "play" else "play"
			if self.control == "pause": self.getAudioThread()
			elif self.control == "play" and self.trackX == self.rightEdge:
				self.recordingStart = 0
				self.trackX = self.leftEdge

	def getAudioThread(self):
		self.t = Thread(target = self.playAudio)
		self.t.start()

	def playAudio(self):
		#taken from source and modified: http://people.csail.mit.edu/hubert/pyaudio/
		song = self.song[self.recordingStart:]

		#below is taken from a module

		p = pyaudio.PyAudio()
		stream = p.open(format=p.get_format_from_width(song.sample_width),  
	                	channels=song.channels,
		                rate=song.frame_rate,
	    	            output=True)

		# break audio into half-second chunks (to allows keyboard interrupts)
		startTime = time.time()
		for chunk in make_chunks(song, 500):
			#modified the area below to suit purposes of the program
			if self.control == "play":
				self.recordingStart += int(round(1000*(time.time() - startTime)))
				stream.stop_stream()
				stream.close()
				p.terminate()
				return
			stream.write(chunk._data)
		self.recordingStart = 0

		stream.stop_stream()  
		stream.close()  

		p.terminate()  


	def drawStatusLine(self,canvas):
		(x0,y0) = (self.trackX,self.cy-self.lineHeight/2)
		(x1,y1) = (self.trackX,self.cy+self.lineHeight/2)
		canvas.create_line(x0,y0,x1,y1,fill="white")

	def onTimerFired(self):
		if self.control == "pause": self.trackX += 1
		if self.trackX >= self.rightEdge:
			self.trackX = self.rightEdge


	def draw(self,canvas):
		self.drawBar(canvas)
		self.drawStatusLine(canvas)
		if self.control == "play": self.drawPlay(canvas)
		elif self.control == "pause": self.drawPause(canvas)

	def drawBar(self,canvas):
		(x0,y0) = (self.leftEdge,self.cy-self.trackHeight/2)
		(x1,y1) = (self.rightEdge,self.cy+self.trackHeight/2)
		canvas.create_rectangle(x0,y0,x1,y1,fill="blue")

	def drawPlay(self,canvas):
		v1 = (self.leftEdge-self.controlWidth - 5,self.cy-self.trackHeight/2)
		v2 = (self.leftEdge-self.controlWidth-5,self.cy+self.trackHeight/2)
		v3 = (self.leftEdge-5,self.cy)
		canvas.create_polygon(v1,v2,v3,fill="purple")

	def drawPause(self,canvas):
		rectangleWidth = self.controlWidth/3
		#creating first rectangle
		r01 = (x01,y01) = (self.leftEdge-self.controlWidth - 5,self.cy-self.trackHeight/2)
		r02 = (x02,y02) = (x01+rectangleWidth,self.cy+self.trackHeight/2)
		canvas.create_rectangle(r01,r02,fill="purple")
		# creating second rectangle
		r11 = (x11,y11) = (x01+2*rectangleWidth-5,y01)
		r12 = (x11+rectangleWidth,y02)
		canvas.create_rectangle(r11,r12,fill="purple")

	def onKeyPressed(self,event):
		if event.keysym == "Up":
			self.song += 1
		elif event.keysym == "Down":
			self.song -= 1

