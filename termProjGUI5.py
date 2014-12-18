# Copyright Anirudh Sridhar. All rights reserved.

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
from analysisClass import ANALYSIS
from saveFileClass import SAVEFILE
from endClass import end


def runMusicDeNoiser():
	musicDeNoiser().run()

class musicDeNoiser(EventBasedAnimationClass):

	#Parent class - manages page classes and facilitates data transfer between classes

	def __init__(self):
		super(musicDeNoiser,self).__init__(500,500)
		self.page = TITLE(self.width,self.height)

	def initAnimation(self):
		self.canvas.bind("<Key>",lambda event: self.onKeyPressedWrapper(event))
		self.canvas.bind("<Motion>",lambda event: self.mouseMotionWrapper(event))
		self.canvas.bind("<Button-1>",lambda event: self.onMousePressedWrapper(event))
		#initializing pages
		titlePage = TITLE(self.width,self.height)
		audioEditPage = audioEdit(self.width,self.height)
		fTPage = fingerTracking(self.width,self.height)
		analysisPage = analysis(self.width,self.height)
		saveFilePage = saveFile(self.width,self.height)
		endPage = end(self.width,self.height)
		self.pages = [titlePage,audioEditPage,fTPage,analysisPage,saveFilePage,endPage]
		self.page = self.pages[0]

	def redrawAll(self):
		self.canvas.delete(ALL)
		self.page.draw(self.canvas)
		if self.page.next != None:
			#changing a page and passing in data to other pages
			self.passVar = self.page.passVar()
			self.page = self.pages[self.page.next]
			self.page.setVar(self.passVar)

	def onKeyPressed(self,event):
		self.page.onKeyPressed(event)

	def onMousePressedWrapper(self,event):
		self.page.onMousePressed(event)
		self.redrawAll()

	def mouseMotionWrapper(self,event):
		self.page.mouseMotion(event)
		self.redrawAll()

	def onTimerFired(self):
		self.timerDelay = self.page.timerDelay
		self.page.onTimerFired()
		self.redrawAll()



class audioEdit(AUDIOEDIT):

	def setVar(self,var):
		#case where it's the first time opening the page
		if type(var) != tuple:
			self.fingerData = var
			startVal = self.fingerData[0][1]
			self.song = AudioSegment.from_wav("originalMusic.wav")[1000*startVal:]
		else: #coming back to the page after modifying audio file
			(self.fingerData,self.song) = var
		self.initAnimation()

	def passVar(self):
		#case where we're done, and need to just save file
		if self.next == 4: return self.song
		#else we need to tell what part of the audio to play
		self.start = float(self.lower-self.leftEdge)/(self.rightEdge-self.leftEdge)*len(self.song)/1000
		#getting relative position in the song
		self.end = float(self.upper-self.leftEdge)/(self.rightEdge-self.leftEdge)*len(self.song)/1000
		return (self.fingerData,self.start,self.end)


class replaceAudioButton(button):

	def initButton(self):
		self.buttonText = "Replace Audio"

class fingerTracking(FINGERTRACKING):

	def passVar(self):
		return self.fingerData


class analysis(ANALYSIS):

	def setVar(self,var):
		(self.fingerData,self.start,self.end) = var
		assert(type(self.fingerData) == list)
		#can only initialize stuff after variables are passed in
		self.initAnalysis()
		self.started = True

	def passVar(self):
		return (self.fingerData,self.song)


class saveFile(SAVEFILE):

	def setVar(self,var):
		self.song = var

           
runMusicDeNoiser()
            
            
            
            
            
