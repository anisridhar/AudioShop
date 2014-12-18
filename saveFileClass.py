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


class SAVEFILE(barePage):

	#saves file and renames it

	def __init__(self,width,height):
		super(SAVEFILE,self).__init__(width,height)
		self.fileText = ""
		self.song = AudioSegment.from_wav("Notes/sa.wav")

	def draw(self,canvas):
		canvas.create_rectangle(0,0,self.width,self.height,fill="black")
		bigText = "Save your creation!"
		font = "Arial 36"
		text = "Type your file name here."
		fileDisplay = self.fileText + ".wav"
		canvas.create_text(self.width/2,self.height*3/4,text=text,fill="white")
		canvas.create_text(self.width/2,self.height*3/4+20,text=fileDisplay,fill="white")
		canvas.create_text(self.width/2,self.height/7,text=bigText,font=font,fill="white")
		imagesDemo1.run(canvas,"saveFileImage.gif",self.width/2,self.height/2,4)

	def onKeyPressed(self,event):
		
		if event.keysym == "BackSpace":
			self.fileText = self.fileText[:-1]
		elif event.keysym == "Return":
			self.saveAs()
			self.next = 5
		else: self.fileText += event.char

	def saveAs(self):
		print type(self.song)
		print self.fileText
		self.song.export(self.fileText + ".wav",format = "wav")
		print "Saved!!!"