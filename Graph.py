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

start_time = time.time()
delay = .1
lineread = []
config = configparser.ConfigParser()
config.read('config.ini')
titles = config.get('SETTINGS', 'graph titles').split(',')
choice = config.get('SETTINGS', 'Input Mode')
sensornum = int(config.get('SETTINGS', 'Number of graphs'))
portName = 'COM11'
baudrate = 9600
curve = []
### START QtApp #####
app = QtGui.QApplication([])  # you MUST do this once (initialize things)

win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window

for x in range(sensornum):
    p = win.addPlot(title=titles[x])  # creates empty space for the plot in the window
    curve.append(p.plot())  # create an empty "plot" (a curve to plot)

windowWidth = 100  # width of the window displaying the curve

# Xm = linspace(0, 0, windowWidth)  # create array that will contain the relevant time series
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
    pool = readTxt("arduino.txt")

pltcount = 0


# Realtime data plot. Each time this function is called, the data display is updated
def update():
    lineread = []
    if choice == "1":
        print("reading data")
        arduinoData = (ser.readline().decode('ascii'))
        lineread = (arduinoData.split(','))
    elif choice == "2":
        arduinoData = next(pool)
        lineread = (arduinoData.split(','))
    elif choice == "3":
        for x in range(sensornum):
            lineread.append(uniform(0, 100))

    outfile = open("output.csv", "a")
    for x in range(sensornum):
        if x == sensornum - 1:
            outfile.write(str(lineread[x]))
        else:
            outfile.write(str(lineread[x]) + ",")

    outfile.write("\n")
    outfile.close()

    for x in range(sensornum):
        global curve, ptr, dataArray

        dataArray[x] = (np.append(dataArray[x], float(lineread[x])))
        dataArray[x] = np.delete(dataArray[x], 0)
        plt = (time.time() - start_time) / delay - windowWidth  # update x position for displaying the curve
        curve[x].setData(dataArray[x])  # set the curve with this data
        curve[x].setPos(plt, 0)  # set x position in the graph to 0

        QtGui.QApplication.processEvents()  # you MUST process the plot now


### MAIN PROGRAM #####
# this is a brutal infinite loop calling your realtime data plot

def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        task()
        next_time += (time.time() - next_time) // delay * delay + delay


every(delay, update)
### END QtApp ####
pg.QtGui.QApplication.exec_()  # you MUST put this at the end
##################
