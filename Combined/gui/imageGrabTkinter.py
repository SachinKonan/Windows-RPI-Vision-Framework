import tkinter as tk
from tkinter import ttk
from tkinter import Entry
import matplotlib
import matplotlib.pylab as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import numpy as np
import time
import sys
from threading import Thread
from PIL import Image, ImageTk
from io import BytesIO


style.use("ggplot")

matplotlib.use("TkAgg")

large_font = ("Verdana", 12)
small_font = ("Verdana", 8)
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

def qf(sting):
    print(sting)

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Start Page", font = large_font)
        label.pack(pady = 10, padx = 10)

        button1 = ttk.Button(self, text = "Visit Stream", command=lambda:controller.show_frame(PageOne))
        button1.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text = "Camera Streamer", font = large_font)
        label.pack(pady = 10, padx = 10)

        button = ttk.Button(self, text = "Back to Home", command=lambda:controller.show_frame(StartPage))
        button.pack()

        button1 = ttk.Button(self, text = "Start Stream", command = self.nuthin)
        button1.pack()

        im = Image.open("aesthetic.png")
        image = ImageTk.PhotoImage(im)
        label = tk.Label(image=image)
        label.pack()

    def nuthin(self):
        pass



app = MainGui()
app.mainloop()
