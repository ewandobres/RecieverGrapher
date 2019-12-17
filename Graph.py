# Import libraries
from random import randrange, uniform
import numpy as np
from PyQt5.QtWidgets import QMainWindow
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
import math
import serial
from itertools import cycle
import configparser
import re

start_time = time.time()
curves = []
lineread = []
config = configparser.ConfigParser()
config.read('config.ini')
titles = config.get('SETTINGS', 'Graph_Titles').split(',')
choice = config.get('SETTINGS', 'Input_Mode')
sensornum = int(config.get('SETTINGS', 'Number_Of_Graphs'))
delay = float(config.get('ARDUINO', 'Input_Delay'))
windowWidth = int(config.get('SETTINGS', 'Data_Width'))
portName = config.get('ARDUINO', 'Port_Name')
baudrate = int(config.get('ARDUINO', 'Baudrate'))
fileName = config.get('SETTINGS', 'File_Name')
testData = config.get('SETTINGS', 'Test_File')
runOnce = 0
### START QtApp #####
app = QtGui.QApplication([])  # you MUST do this once (initialize things)


def removeIllegalChars(inp):
    result = re.sub("[^0-9,.]", "", inp)
    return result
windowWidthZoomed = windowWidth

class MyWindow(pg.GraphicsWindow):


    def __init__(self, **kargs):
        super().__init__(**kargs)




    def wheelEvent(self, event):



        for x in range(len(curves)):
            if self.getItem(0, x).isUnderMouse():
                print("I'm over " + str(x))

        QtGui.QGraphicsView.wheelEvent(self, event)




win = MyWindow(title="Signal from serial port", size=(1920, 1080))  # creates a window

class Curve():

    def __init__(self, selftitle):
        self.windowWidthZoomed = windowWidth
        self.title = selftitle
        self.curvegraph = win.addPlot(title=selftitle).plot()

    def zoomIn(self):
        self.windowWidthZoomed -= 1

    def zoomOut(self):
        self.windowWidthZoomed += 1



# check config is valid
if sensornum != len(titles):
    print("You have given the incorrect number of titles for the number of graphs. Check config.ini. ")
    exit()




for x in range(sensornum):

    curves.append(Curve(titles[x]))
    curves[x].curvegraph.scale(delay, 1)

ptr = -windowWidth  # set first x position
dataArray = []
largeArray = [sensornum]
for x in range(sensornum):
    dataArray.append(np.linspace(0, 0, windowWidth))


sensor = []
lines = []
if choice == "1":
    try:
        ser = serial.Serial(portName, baudrate)
    except:
        print("Couldn't connect to serial port, have you entered it correctly? Is the arduino plugged in?")
        exit()
elif choice == "2":
    f = open(testData, 'r')
    textdata = f.readlines()
    f.close
    pool = cycle(textdata)

pltcount = 0


# Realtime data plot. Each time this function is called, the data display is updated
def update():
    lineread = []
    if choice == "1":
        print("reading data")
        arduinoData = (ser.readline().decode('ascii'))
        lineread = (arduinoData.split(','))
    elif choice == "2":
        tempRead = next(pool)
        arduinoData = removeIllegalChars(tempRead)
        lineread = (arduinoData.split(','))
    elif choice == "3":
        for x in range(sensornum):
            lineread.append(uniform(0, 100))

    if len(lineread) == sensornum:
        outfile = open(fileName, "a")
        for x in range(sensornum):
            if x == sensornum - 1:
                outfile.write(str(lineread[x]))
            else:
                outfile.write(str(lineread[x]) + ",")

        outfile.write("\n")
        outfile.close()

        for x in range(sensornum):
            global Curve, ptr, dataArray, runOnce

            dataArray[x] = (np.append(dataArray[x], float(lineread[x])))
            dataArray[x] = np.delete(dataArray[x], 0)

            curves[x].curvegraph.setData(dataArray[x][:curves[x].windowWidthZoomed])  # set the curve with this data
            curves[x].curvegraph.setPos(currenttime() - windowWidth * delay, 0)

            QtGui.QApplication.processEvents()  # you MUST process the plot now


### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot

def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        task()
        next_time += (time.time() - next_time) // delay * delay + delay


def currenttime():
    return round(time.time() - start_time, 2)


every(delay, update)
### END QtApp ####
pg.QtGui.QApplication.exec_()  # you MUST put this at the end
##################
