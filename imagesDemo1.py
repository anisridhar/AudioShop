# imagesDemo1.py
# view in canvas
# read from file
# with transparent pixels
# get size, resize (zoom and subsample)

# image resized, made transparent with:
# http://www.online-image-editor.com/

#Taken from 15-112 course notes and modified

from Tkinter import *


def redrawAll(canvas,x,y):
    font = ("Arial", 16, "bold")
    msg = "Image Demo #1 (read from file)"
    image = canvas.data["img"]
    canvas.create_image(x, y, image=image)

def init(canvas,path,x,y,scale):
    image = PhotoImage(file=path)
    canvas.data["img"] = image

    newImage = image.subsample(scale,scale)
    canvas.data["img"] = newImage

    redrawAll(canvas,x,y)

########### copy-paste below here ###########

def run(canvas,path,x,y,scale):

    canvas.data = { }
    init(canvas,path,x,y,scale)
