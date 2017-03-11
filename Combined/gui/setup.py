import cx_Freeze
import sys
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\Sachin Konan\\Documents\Python\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Sachin Konan\\Documents\Python\\tcl\\tk8.6"

base = None
base = "Win32GUI"

executables = [cx_Freeze.Executable("imageGrabTkinterUDP.py", base=base )]

cx_Freeze.setup(
    name = "ImageGrabberUDP",
    options = {"build_exe": {"packages":["tkinter","matplotlib", "PIL", "time", "cv2" , "socket"], "include_files":["aesthetic.png"]}},
    version = "0.01",
    description = "MJPEG Grabber for Python 3.5",
    executables = executables
    )