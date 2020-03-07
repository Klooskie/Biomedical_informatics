# AGH UST Medical Informatics 03.2020
# Lab 1 : DICOM

import pydicom
from tkinter import *
from PIL import Image, ImageTk

class MainWindow():

    ds = pydicom.dcmread("./data/head.dcm")
    data = ds.pixel_array

    def __init__(self, main):
        # print patient name
        print(self.ds.PatientName)

        # prepare canvas
        self.canvas = Canvas(main, width=512, height=512)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.initWindow)
        self.canvas.bind("<B1-Motion>", self.updateWindow)
        self.canvas.bind("<Button-3>", self.initMeasure)
        self.canvas.bind("<B3-Motion>", self.updateMeasure)
        self.canvas.bind("<ButtonRelease-3>", self.finishMeasure)

        # load image
        # todo: apply transform
        #self.array = self.transformData(self.data, self.winWidth, self.winCenter)
        self.array = self.data
        self.image = Image.fromarray(self.array)
        self.image = self.image.resize((512, 512), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image=self.image, master=root)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.img)


    def transformData(self, data, window, level):
        # todo: transform data
        return data


    def initWindow(self, event):
        # todo: save mouse position
        print("x: " + str(event.x) + " y: " + str(event.y))

    def updateWindow(self, event):
        # todo: modify window width and center
        print("x: " + str(event.x) + " y: " + str(event.y))
        #self.array2 = self.transformData(self.data, self.winWidth, self.winCenter)
        #self.image2 = Image.fromarray(self.array2)
        #self.image2 = self.image2.resize((512, 512), Image.ANTIALIAS)
        #self.img2 = ImageTk.PhotoImage(image=self.image2, master=root)
        #self.canvas.itemconfig(self.image_on_canvas, image = self.img2)


    def initMeasure(self, event):
        # todo: save mouse position
        # todo: create line
        # hint: self.canvas.create_line(...)
        print("x: " + str(event.x) + " y: " + str(event.y))

    def updateMeasure(self, event):
        # todo: update line
        # hint: self.canvas.coords(...)
        print("x: " + str(event.x) + " y: " + str(event.y))

    def finishMeasure(self, event):
        # todo: print measured length in mm
        print("x: " + str(event.x) + " y: " + str(event.y))



#----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()
