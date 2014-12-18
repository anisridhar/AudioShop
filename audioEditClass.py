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




class AUDIOEDIT(barePage):

	#displays recording, allows user to hear it, interact with trackbar, and highlight
	# sections they want denoised

	def __init__(self,width,height):
		super(AUDIOEDIT,self).__init__(width,height)

	def initAnimation(self):
		self.next = None
		#track bar attributes
		self.leftEdge = self.width/4
		self.rightEdge = 3*self.width/4
		self.trackHeight = 30
		#initializing track bar line location
		self.trackX = self.leftEdge
		self.lineHeight = 2*self.trackHeight
		#initializing control settings
		self.control = "play"
		self.controlWidth = self.trackHeight
		#initializing button dimensions
		self.buttonWidth = 30
		#initializing recording settings
		self.recordingStart = 0
		self.timerDelay = int(round(float(len(self.song)/(self.rightEdge-self.leftEdge))))
		#initializing track selection settings
		self.gotLower = self.gotUpper = False
		self.lower = self.upper = 0
		self.skip = False


	def draw(self,canvas):
		self.drawInterface(canvas)
		#drawing track bar
		self.drawTrackBar(canvas)
		if self.control == "pause": self.drawPause(canvas)
		elif self.control == "play": self.drawPlay(canvas)
		self.makeButton1(canvas)

	def drawInterface(self,canvas):
		#draws text/images
		canvas.create_rectangle(0,0,self.width,self.height,fill="black")
		text0 = "Denoise your music!"
		font0 = "Arial 30"
		text1 = """
		Press space to begin highlighting the portion you want to denoise, 
		and space to end the highlighting.

		You can also click the trackbar to skip portions of the recording.
		"""
		canvas.create_text(self.width/2,self.height/8,text=text0,font=font0,fill="white")
		canvas.create_text(self.width/2-80,self.height/4,text=text1,fill="white")
		imagesDemo1.run(canvas,"denoiseImage.gif",self.width/2,self.height*3/4,3)
		canvas.create_text(self.width/2,self.height*3/4+75,text="Denoise it!",fill="white")


	def drawTrackBar(self,canvas):
		#draws track bar
		(x0,y0) = (self.leftEdge,self.height/2-self.trackHeight/2)
		(x1,y1) = (self.rightEdge,self.height/2+self.trackHeight/2)
		canvas.create_rectangle(x0,y0,x1,y1,fill="blue",outline="blue")
		self.drawStatusLine(canvas)
		if self.gotLower: #have started highlighting track
			self.drawHighlightedArea(canvas)

	def drawHighlightedArea(self,canvas):
		#draws rectangle overlay to indicate highlighted portion
		(x0,y0) = (self.lower,self.height/2+self.trackHeight/2)
		(x1,y1) = (self.upper,self.height/2-self.trackHeight/2)
		canvas.create_rectangle(x0,y0,x1,y1,outline="red",fill="red")

	def drawStatusLine(self,canvas):
		#shows progress in the piece
		(x0,y0) = (self.trackX,self.height/2-self.lineHeight/2)
		(x1,y1) = (self.trackX,self.height/2+self.lineHeight/2)
		canvas.create_line(x0,y0,x1,y1,fill="white")

	def onTimerFired(self):
		if self.control == "pause": self.trackX += 1
		if self.trackX >= self.rightEdge:
			self.trackX = self.rightEdge
		#highlighting portions of the trackbar
		if self.gotLower and not self.gotUpper and self.control == "pause":
			self.upper += 1



	def drawPlay(self,canvas):
		#draws play symbol
		v1 = (self.leftEdge-self.controlWidth - 5,self.height/2-self.trackHeight/2)
		v2 = (self.leftEdge-self.controlWidth-5,self.height/2+self.trackHeight/2)
		v3 = (self.leftEdge-5,self.height/2)
		canvas.create_polygon(v1,v2,v3,fill="purple")

	def drawPause(self,canvas):
		#draws pause symbol
		rectangleWidth = self.controlWidth/3
		#creating first rectangle
		r01 = (x01,y01) = (self.leftEdge-self.controlWidth - 5,self.height/2-self.trackHeight/2)
		r02 = (x02,y02) = (x01+rectangleWidth,self.height/2+self.trackHeight/2)
		canvas.create_rectangle(r01,r02,fill="purple")
		#creating second rectangle
		r11 = (x11,y11) = (x01+2*rectangleWidth-5,y01)
		r12 = (x11+rectangleWidth,y02)
		canvas.create_rectangle(r11,r12,fill="purple")

	def onMousePressed(self,event):
		#controlling play/pause button
		if (self.leftEdge-self.controlWidth-5 <= event.x <= self.leftEdge-5 and 
			self.height/2-self.trackHeight/2 <= event.y <= self.height/2+self.trackHeight/2):
			self.control = "pause" if self.control == "play" else "play"
			if self.control == "pause": self.getAudioThread()
			elif self.control == "play" and self.trackX == self.rightEdge:
				self.recordingStart = 0
				self.trackX = self.leftEdge
		v0 = (x,y) = (self.width/2-50,self.height*3/4-50)
		v1 = (x+100,y+100)
		#controlling status of trackBar
		if (self.leftEdge <= event.x <= self.rightEdge and
			self.height/2-self.trackHeight/2 <= event.y <= self.height/2+self.trackHeight/2):
			self.skip = True
			self.trackX = self.upper = event.x
			self.recordingStart = int(round(float(self.trackX-self.leftEdge)/(self.rightEdge-self.leftEdge)*len(self.song)))
			self.getAudioThread()
		#checking if button is clicked
		elif v0[0] <= event.x <= v1[0] and v0[1] <= event.y <= v1[1]:
			self.next = 3
		elif self.buttonx0 <= event.x <= self.buttonx1 and self.buttony1 <= event.y <= self.buttony0:
			self.next = 3

	def onKeyPressed(self,event):
		#highlighting section
		if event.keysym == "space":
			if self.gotLower == False:
				self.gotLower = True
				self.lower = self.upper = self.trackX
			elif self.gotUpper == False:
				self.gotUpper = True
				self.upper = self.trackX
		elif event.keysym == "Right": #going to saveFile page
			self.next = 4



	def makeButton1(self,canvas):
		#draws button
		v1 = (self.buttonx0,self.buttony0) = (5,self.height - 5)
		(x0,y0) = (self.buttonx0,self.buttony0)
		v2 = (self.buttonx1,self.buttony1) = (x0+self.buttonWidth,y0-self.buttonWidth)
		(cx,cy) = (x0+self.buttonWidth/2,y0+self.buttonWidth/2)
		canvas.create_rectangle(v1,v2,fill="green")

	def getAudioThread(self):
		self.t = Thread(target = self.playAudio)
		self.t.start()

	def playAudio(self):
		#base code taken from http://people.csail.mit.edu/hubert/pyaudio/ and heavily modified
		print self.recordingStart
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
			elif self.skip == True:
				self.skip = False
				stream.stop_stream()
				stream.close()
				p.terminate()
				return 
			stream.write(chunk._data)
		self.recordingStart = 0

		stream.stop_stream()  
		stream.close()  

		p.terminate()  