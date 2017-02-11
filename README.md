# Windows-RPI-Vision-Framework

This project was created to aid remote vision development on processors such as the Raspberry PI or the Odroid. The system works by using threading to simultaneously process and send an image to a mjpeg http stream over the Internet. On one's computer, a GUI will grab an image based on the encoded url and display the image in a Tkinter Python GUI.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing Dependencies


1. OpenCV on Deployed System (Raspberry PI)
 - I suggest you follow this tutorial: http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/. Make sure that in the last step, you compile the code with one core; it never works with all 4.
 ```
 The command is: make
 Not: make-j4
 ```

2. OpenCV on Computer
 - As I am a Python 3 advocate, you will need to install OpenCV3 on your desktop. Not sure about MAC Users, but for Ubuntu and Windows users you need to download the wheel file from this link: http://www.lfd.uci.edu/~gohlke/pythonlibs/. Control-F on the webpage for the OpenCV package and download the right version based on the bit number for PYTHON not Windows. IF you have 32 bit python on 64 bit windows, still download the 32 bit version. You can get the contrib version if you want, I think I have that, but it shouldn't matter for this application. Once downloaded, open Command Prompt from wherever you have stored your wheel (probably in downloads) and type in:

 ```
 pip install opencv_python_........ <--- Thats the rest of your wheel
 ```

3. Download Numpy
 - On the RPI, you will want to go into the virtual environment you created in Step 1 by typing:
 ```
 source ~/.profile
 workon cv
 ```
 Then typing:
 ```
 sudo pip install numpy
 ```
4. Download Putty on Control computer
 - Download Putty.exe from this link: http://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html, and follow the relatively simple install.

## Authors

* **Sachin Konan** - *Initial work* - [SachinKonan](https:/github.com/SachinKonan)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Project was inspired by vision processing in the First Robotics Competition, but has promising applications for general computer vision testing.
