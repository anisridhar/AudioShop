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


class FINGERTRACKING(barePage):

	#base code for single color tracking taken from source:
	## Copyright (c) 2013-2014 Abid K and Jay Edry
## You may use, redistribute and/or modify this program it under the terms of the MIT license (https://github.com/abidrahmank/MyRoughWork/blob/master/license.txt).
# I have modified single color tracking heavily to detect objects of different sizes
# and multiple colors and record data simultaneously. 


	def __init__(self,width,height):
		super(FINGERTRACKING,self).__init__(width,height)
		#color sensing bounds
		self.gLower = 30 
		self.gUpper = 100 
		self.greenMin = np.array((self.gLower,100,100))
		self.greenMax = np.array((self.gUpper,255,255))
		self.bLower = 100 
		self.bUpper = 115 
		self.blueMin = np.array((self.bLower,100,100))
		self.blueMax = np.array((self.bUpper,255,255))
		self.rLower = 120 
		self.rUpper = 180 
		self.redMin = np.array((self.rLower,100,100))
		self.redMax = np.array((self.rUpper,255,255))
		#initializing finger analysis stuff
		self.fingerVals = [0]*5
		self.startVal = False
		self.stopVal = False
		self.time = 0
		self.stopped = False
		self.c = cv2.VideoCapture(0)
		self.oldVals = None
		self.fingerData = []


	def onMousePressed(self,event):
		#doing buttonpressed
		x = self.width/2
		y = self.height-100
		v0 = (x-50,y-50)
		v1 = (x+50,y+50)
		if not(v0[0] <= event.x <= v1[0] and v0[1] <= event.y <= v1[1]):
			return
		if self.startVal == False: 
			self.startVal = True
			self.time = time.time()
		else: self.stopVal = True

	def draw(self,canvas):
		#draws interface before video is launched, including countdown
		if self.startVal == False:
			self.drawInstructions(canvas)
		self.timeDif = time.time() - self.time
		if self.startVal == True:# and self.timeDif > 0:
			text = str(5 - int(round(self.timeDif)))
			self.timerPage(canvas)
			font = "Arial 28"
			canvas.create_text(self.width/2,self.height/2,text=text,font=font,fill="white")

	def timerPage(self,canvas):
		#displaying recording countdown
		canvas.create_rectangle(0,0,self.width,self.height,fill="black")
		text = "Recording in"
		font = "Arial 30"
		canvas.create_text(self.width/2,self.height/3,text=text,font=font,fill="white")

	def drawInstructions(self,canvas):
		#draws interface before recording sequence starts
		canvas.create_rectangle(0,0,self.width,self.height,fill="black")
		#create button
		(cx,cy) = (self.width/2,self.height - 100)
		r = 20
		r1 = 15
		r2 = 10
		imagesDemo1.run(canvas,"recordImage.gif",cx,cy,3)
		text = "Click the record button to start capturing Video and Audio."
		text1 = "Record your music!"
		font1 = "Arial 30"
		canvas.create_text(self.width/2,self.height/2,text=text,fill="white")
		canvas.create_text(self.width/2,self.height/8,text=text1,fill="white",font=font1)

	def onTimerFired(self):
		c = self.c
		if self.startVal == True and self.timeDif > 5:
			self.getRecordingThread()
			self.runModule()
			#after video capture, change pages
			self.next = 1

		
	def getThresholdedImg(self):
		#basic structure taken from color ball tracking code - have modified parameters
		green = cv2.inRange(self.hsv,self.greenMin,self.greenMax)
		blue = cv2.inRange(self.hsv,self.blueMin,self.blueMax)
		red = cv2.inRange(self.hsv,self.redMin,self.redMax)
		self.colors = cv2.add(green,blue)
		self.colors = cv2.add(red,self.colors)
		return self.colors


	def runModule(self):
		c = self.c
		self.width,self.height = self.c.get(3),self.c.get(4)
		startTime = time.time()

		while(1): #taken from module

			_,f = c.read()
			f = cv2.flip(f,1)

			blur = cv2.medianBlur(f,5)
			self.hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
			both = self.getThresholdedImg()
			erode = cv2.erode(both,None,iterations = 3)
			dilate = cv2.dilate(erode,None,iterations = 10)

			self.f = f

			self.contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
			#below is all my modifications and work - drawing thresholding bounds for 
			#finger tracking, detecting and recording notes
			(self.x0,self.y0,self.x1,self.y1) = self.drawGrid()

			self.note = self.trackColors()

			if self.note != self.oldVals and type(self.note) == str:
				self.oldVals = self.note
				timeDif = time.time() - startTime
				self.fingerData += [(self.note,timeDif)]
				print self.note
			elif (self.note,self.oldVals) == ("ga","sa") or (self.note,self.oldVals) == ("sa","ga"):
				self.note = "ri"
				self.oldVals = self.note
				timeDif = time.time() - startTime
				self.fingerData += [(self.note,timeDif)]
				print self.note


			# re-initializing self.fingerVals
			self.fingerVals = [1]*5


			cv2.imshow("img",self.f)

			if cv2.waitKey(25) == 27:
				self.stopVal = True
				self.startVal = False
				break

		print self.fingerData

		cv2.destroyAllWindows()
		c.release()

	def trackColors(self):
		#tracks colors for right hand, tracks blob sizes for left hand
		blobCount = 0
		blobSizes = []
		isGa = False
		gotNote = False
		for cnt in self.contours:
			x,y,w,h = cv2.boundingRect(cnt)
			cx,cy = x + w/2, y + h/2
			self.cx,self.cy = cx,cy
			if not(self.x0<=cx<=self.x1 and self.y0<=cy<=self.y1): continue
			if w <= 50 or h <= 50: continue
			(centerX,centerY) = (self.width/2,self.height/2)
			if cx >= centerX: color = [0,255,0]
			else: color = [255,0,0]
			color = [0,0,255] if cy <= self.height/2 else color
			#find green

			if self.gLower <= self.hsv.item(cy,cx,0) <= self.gUpper:
				cv2.rectangle(self.f,(x,y),(x+w,y+h),color,2)
				if cy <= self.height/2 and cx >= self.width/2:
					self.fingerVals[4] = 0
				elif cy >= self.height/2 and cx >= self.width/2:
					self.fingerVals[4] = 1
					gotNote = True
					# print "pa"
			elif self.bLower <= self.hsv.item(cy,cx,0) <= self.bUpper:
				cv2.rectangle(self.f,(x,y),(x+w,y+h),color,2)
				if cy <= self.height/2 and cx >= self.width/2:
					self.fingerVals[3] = 0
				elif cy >= self.height/2 and cx >= self.width/2:
					self.fingerVals[3] = 1
					gotNote = True

			if gotNote: continue


			# find blue
			if self.bLower < self.hsv.item(cy,cx,0) < self.bUpper and not gotNote and cx <= self.width/2:
				cv2.rectangle(self.f,(x,y),(x+w,y+h),color,2)
				if self.cy <= self.height/2 and cx <= self.width/2:
					blobCount += 1
					blobSizes += [w]

		RH = self.fingerVals[3:]
		if RH == [1,1]: return "pa"
		elif RH == [1,0]: return "da"
		# else: print RH
		# print "blobFat = ", sum(blobSizes)
		if sum(blobSizes) <= 180: return "sa"
		elif sum(blobSizes) <= 230: return "ri"
		else: return "ga"

		if blobCount == 3: return "ga"
		elif blobCount == 2:
			for c in blobSizes:
				if c >= 250:
					isGa = True
					return "ga"
			if not isGa: return "ri"
		elif blobCount == 1:
			for c in blobSizes:
				if c >= 250:
					return "ga"
				elif 190 <= c <= 230:
					return "ri"
				else: return "sa"



	def drawGrid(self):
		c = self.c
		(cx,cy) = (int(self.width/2),int(self.height/2))
		(w,h) = (int(3*self.width/4),int(3*self.height/4))
		cv2.rectangle(self.f,(cx-w/2,cy-h/2),(cx+w/2,cy+h/2),[255,255,255],2)
		cv2.line(self.f,(cx,cy-h/2),(cx,cy+h/2),[255,255,255],2)
		cv2.line(self.f,(cx-w/2,cy),(cx+w/2,cy),[255,255,255],2)
		return (cx-w/2,cy-h/2,cx+w/2,cy+h/2)


	def getRecordingThread(self):
		self.t = Thread(target = self.getRecording)
		self.t.start()

	def getRecording(self):

		#taken from source and modified: http://people.csail.mit.edu/hubert/pyaudio/

		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = 20
		WAVE_OUTPUT_FILENAME = "originalMusic.wav"

		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,
						frames_per_buffer=CHUNK)
		print("* recording")
		frames = []
		while not self.stopVal:
			data = stream.read(CHUNK)
			frames.append(data)
		print "* done recording"
		stream.stop_stream()
		stream.close()
		p.terminate()

		if os.path.exists("originalMusic.wav"):
			print "removed!"
			os.remove("originalMusic.wav")


		wf = wave.open(WAVE_OUTPUT_FILENAME	,"wb")
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()
		print "finished!"

	
