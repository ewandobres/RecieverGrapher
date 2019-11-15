# Import libraries
from itertools import cycle
from random import randrange, uniform
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
import math

start_time = time.time()
delay = .2

# Create object serial port
portName = "COM12"  # replace this port name by yours!
baudrate = 9600
 ser = serial.Serial(portName, baudrate)
# assume that the first 3 inputs are the accelerometer values
sensornum = 3 #num of graphs
inputs = 5 #num of raw inputs
curve = []
### START QtApp #####
app = QtGui.QApplication([])  # you MUST do this once (initialize things)

win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window

for x in range(sensornum):
    p = win.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
    curve.append(p.plot())  # create an empty "plot" (a curve to plot)

windowWidth = 100  # width of the window displaying the curve

# Xm = linspace(0, 0, windowWidth)  # create array that will contain the relevant time series
ptr = -windowWidth  # set first x position
dataArray = []
for x in range(sensornum):
    dataArray.append(np.linspace(0, 0, windowWidth))

timesense = []
loopnum = 0
sensor = []
lines = []

#f = open("testdata.txt")

#for x in f:
    #lines.append(x)


#f.close()
#pool = cycle(lines)

pltcount = 0


# Realtime data plot. Each time this function is called, the data display is updated
def update():

    lineread = []
    value = []
    arduinoData = ser.readline()
    lineread = (arduinoData.split(','))
    for x in lineread:
        x = float(x)





    #for x in range(inputs):
       #lineread.append(uniform(0, 100))

    acc = calcAcceleration(lineread[0], lineread[1], lineread[2])
    newLineread = []
    newLineread.append(acc)
    newLineread.append(lineread[3:])

    outfile = open("output.csv", "a")
    for x in range(sensornum):
        if x == sensornum -1:
            outfile.write(str(lineread[x]))
        else:
            outfile.write(str(lineread[x])+ ",")


    outfile.write("\n")
    outfile.close()
    #
    for x in range(sensornum):
        global curve, ptr, dataArray

        plt = []
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



def calcAcceleration(x, y, z):
    x = int(x)
    y = int(y)
    z = int(z)
    result = math.sqrt(x**2+y**2+z**2)
    return result

every(delay, update)
### END QtApp ####
pg.QtGui.QApplication.exec_()  # you MUST put this at the end
##################
