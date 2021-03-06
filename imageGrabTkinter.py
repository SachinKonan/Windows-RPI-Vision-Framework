import tkinter as tk
from tkinter import ttk
import matplotlib
from matplotlib import style
from PIL import Image, ImageTk
import time
import cv2 as cv2


large_font = ("Verdana", 12)
small_font = ("Verdana", 8)

ip = '10.54.65.58'
url1 = 'http://' + ip + ':5810/stream.mjpg'

class MainGui(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "FRC Camera Streamer", font = large_font)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "Visit Stream", command=lambda:controller.show_frame(PageOne))
        button1.pack()
        im = Image.open("Combined\\gui\\robot.jpg")
        photo = ImageTk.PhotoImage(im)

        self.labelImage = tk.Label(self, image=photo)
        self.labelImage.image = photo  # keep a reference!
        self.labelImage.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Camera Streamer", font = large_font)
        label.pack(pady = 10, padx = 10)

        button = ttk.Button(self, text = "Back to Home", command=lambda:controller.show_frame(StartPage))
        button.pack()

        self.statuslabel = tk.Label(self,text = "STATUS IS: Not streaming", font=small_font)
        self.statuslabel.pack()

        im = Image.open("Combined\\gui\\aesthetic.png")
        photo = ImageTk.PhotoImage(im)

        self.labelImage = tk.Label(self, image=photo)
        self.labelImage.image = photo  # keep a reference!
        self.labelImage.pack()

        frame = tk.Frame(self)
        frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        chan1 = ttk.Button(frame, text="Start Stream ", command= self.startStream)
        chan1.pack(side= tk.LEFT,pady=20, padx=20)

        chan2 = ttk.Button(frame, text="Stop Stream", command= self.stopStream)
        chan2.pack(side= tk.RIGHT,pady=20, padx=20)
        self.url = url1
        self.cap = None

    def changeStream(self):
        pass
    def startStream(self):

        self.statuslabel['text'] = 'STATUS: Starting Server'
        self.cap = cv2.VideoCapture(self.url)

        if (self.cap.isOpened()):
            self.statuslabel['text'] = 'STATUS: MJPEG IS UP'
            self.repeatShow()
        else:
            self.statuslabel['text'] = 'STATUS: MJPEG IS DOWN'

    def repeatShow(self):
        if(self.cap.isOpened()):
            ret,img = self.cap.read()

            image = Image.fromarray(img)
            image1 = ImageTk.PhotoImage(image)
            self.labelImage['image']=image1
            self.labelImage.image = image1
        else:
            im = Image.open("Combined\\gui\\aesthetic.png")
            photo = ImageTk.PhotoImage(im)

            self.labelImage['image'] = photo
            self.labelImage.image = photo
            return

        self.after(ms=1, func=lambda: self.repeatShow())

    def stopStream(self):
        self.statuslabel['text'] = 'STATUS: LEFT Ongoing STREAM'
        self.cap.release()


app = MainGui()
app.mainloop()
