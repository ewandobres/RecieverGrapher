# Import libraries
from random import randrange, uniform
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
import math
import serial
from itertools import cycle
import configparser
import re

start_time = time.time()

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
curve = []
### START QtApp #####
app = QtGui.QApplication([])  # you MUST do this once (initialize things)


def removeIllegalChars(inp):
    result = re.sub("[^0-9,.]", "", inp)
    return result


# check config is valid
if sensornum != len(titles):
    print("You have given the incorrect number of titles for the number of graphs. Check config.ini. ")
    exit()

win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window

for x in range(sensornum):
    createPlotSpace = win.addPlot(title=titles[x])  # creates empty space for the plot in the window
    curve.append(createPlotSpace.plot())  # create an empty "plot" (a curve to plot)
    curve[x].scale(delay, 1)

ptr = -windowWidth  # set first x position
dataArray = []
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
            global curve, ptr, dataArray, runOnce

            dataArray[x] = (np.append(dataArray[x], float(lineread[x])))
            dataArray[x] = np.delete(dataArray[x], 0)
            curve[x].setData(dataArray[x])  # set the curve with this data
            curve[x].setPos(currentTime() - windowWidth * delay, 0)
            QtGui.QApplication.processEvents()  # you MUST process the plot now
    else:
        print("Error: Either an empty input has been detected or incorrect number of inputs specified")

### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot

def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        task()
        next_time += (time.time() - next_time) // delay * delay + delay


def currentTime():
    return round(time.time() - start_time, 2)


every(delay, update)
### END QtApp ####
pg.QtGui.QApplication.exec_()  # you MUST put this at the end
##################
