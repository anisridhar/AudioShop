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

class end(barePage):

	#ending page, file naming

	def draw(self,canvas):
		canvas.create_rectangle(0,0,self.width,self.height,fill="black")
		imagesDemo1.run(canvas,"enjoyImage.gif",self.width/2,self.height/2,2)
		font = "Arial 36"
		canvas.create_text(self.width/2,self.height/8,text="File Saved!",font=font,fill="white")