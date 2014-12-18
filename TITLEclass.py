from barePageClass import barePage
from buttonClass import button
import imagesDemo1

class TITLE(barePage):

	#title page - splash screen

	def __init__(self,width,height):
		super(TITLE,self).__init__(width,height)
		self.initTitle()

	def initTitle(self):
		self.button = startButton("purple",self.width/2,self.height*3/4,50,50)

	def draw(self,canvas):
		canvas.create_rectangle(0,0,self.width,self.height,fill="black")
		text = "AudioShop"
		font = "Arial 36"
		canvas.create_text(self.width/2,self.height/5,text=text,fill="white",font=font)
		imagesDemo1.run(canvas,"titleImage.gif",self.width/2,self.height/2,3)
		self.button.draw(canvas)

	def onMousePressed(self,event):
		self.button.onMousePressed(event)
		self.next = self.button.next #switches page when button is pressed

class startButton(button):

	def initButton(self):
		self.buttonText = "Go!"

	def onMousePressed(self,event):
		super(startButton,self).onMousePressed(event)
		if self.buttonPressed: self.next = 2