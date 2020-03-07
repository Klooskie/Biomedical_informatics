# AGH UST Medical Informatics 03.2020
# Lab 1 : DICOM

import pydicom
from math import sqrt
from tkinter import *
from PIL import Image, ImageTk


class MainWindow:
    ds = pydicom.dcmread("./data/head.dcm")
    data = ds.pixel_array

    def __init__(self, main):
        # print patient name
        print(self.ds.PatientName)

        self.winCenter = self.ds.WindowCenter
        self.winWidth = self.ds.WindowWidth
        self.pixelSpacing = self.ds.PixelSpacing
        self.line = None

        print("Window width is:", self.winWidth)
        print("Window center is:", self.winCenter)

        # prepare canvas
        self.canvas = Canvas(main, width=512, height=512)
        self.canvas.grid(row=0, column=0)
        self.canvas.bind("<Button-1>", self.initWindow)
        self.canvas.bind("<B1-Motion>", self.updateWindow)
        self.canvas.bind("<Button-3>", self.initMeasure)
        self.canvas.bind("<B3-Motion>", self.updateMeasure)
        self.canvas.bind("<ButtonRelease-3>", self.finishMeasure)

        # load image
        # apply transform
        self.array = self.transformData(self.data, self.winWidth, self.winCenter)
        # self.array = self.data
        self.image = Image.fromarray(self.array)
        self.image_size = self.image.size
        self.image = self.image.resize((512, 512), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image=self.image, master=root)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.img)

    def transformData(self, data, window, level):
        window_start = level - window / 2
        data = ((data - window_start) / window) * 255
        return data

    def initWindow(self, event):
        # save mouse position
        self.mouse_pos = event.x, event.y
        # print("x: " + str(event.x) + " y: " + str(event.y))

    def updateWindow(self, event):
        # modify window width and center
        self.winCenter += self.mouse_pos[1] - event.y
        self.winWidth += event.x - self.mouse_pos[0]
        self.mouse_pos = event.x, event.y

        self.array2 = self.transformData(self.data, self.winWidth, self.winCenter)
        self.image2 = Image.fromarray(self.array2)
        self.image2 = self.image2.resize((512, 512), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(image=self.image2, master=root)
        self.canvas.itemconfig(self.image_on_canvas, image=self.img2)
        # print("x: " + str(event.x) + " y: " + str(event.y))

    def initMeasure(self, event):
        # save mouse position
        self.start_line_mouse_pos = event.x, event.y
        # create line
        if self.line:
            self.canvas.delete(self.line)
        self.line = self.canvas.create_line(self.start_line_mouse_pos, event.x, event.y, fill='red')
        # print("x: " + str(event.x) + " y: " + str(event.y))

    def updateMeasure(self, event):
        # save mouse position
        self.mouse_pos = event.x, event.y
        # update line
        self.canvas.coords(self.line, *self.start_line_mouse_pos, *self.mouse_pos)
        # print("x: " + str(event.x) + " y: " + str(event.y))

    def finishMeasure(self, event):
        # print measured length in mm
        x_diff = (event.x - self.start_line_mouse_pos[0]) * self.pixelSpacing[1] / (512 / self.image_size[0])
        y_diff = (event.y - self.start_line_mouse_pos[1]) * self.pixelSpacing[0] / (512 / self.image_size[1])
        dist = sqrt(x_diff ** 2 + y_diff ** 2)
        print("Distance is: " + str(dist) + "mm")
        # print("x: " + str(event.x) + " y: " + str(event.y))


# ----------------------------------------------------------------------

root = Tk()
MainWindow(root)
root.mainloop()
