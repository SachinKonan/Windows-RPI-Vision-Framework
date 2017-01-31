from urllib.request import urlopen
html = urlopen("http://127.0.0.1:9090/cam.mjpg")
print(html)