# Import libraries
from itertools import cycle
from random import randrange, uniform
from numpy import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
import threading



start_time = time.time()
delay = .1


# Create object serial port
portName = "COM12"  # replace this port name by yours!
baudrate = 9600
# ser = serial.Serial(portName, baudrate)

sensornum = 1
curve = []
### START QtApp #####
app = QtGui.QApplication([])  # you MUST do this once (initialize things)


win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window

for x in range(sensornum):
    p = win.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
    curve.append(p.plot())  # create an empty "plot" (a curve to plot)


windowWidth = 10  # width of the window displaying the curve

Xm = linspace(0, 0, windowWidth)  # create array that will contain the relevant time series
ptr = -windowWidth  # set first x position

timesense = []
count = -1
nums = []
loopnum = 0

sensor = []

lines = []

#f = open("testdata.txt")
#for x in f:
#    lines.append(x)

#pool = cycle(lines)

pltcount = 0

# Realtime data plot. Each time this function is called, the data display is updated
def update():
    global pltcount
    pltcount += 1
    lineread = []
    #arduinoData = next(pool)
    #lineread = (arduinoData.split(','))
    for x in range(sensornum):
        lineread.append(uniform(0, 100))
    #timesense = lineread(len(lineread)-1)

    for x in range(sensornum):

        global curve, ptr, Xm

        Xm[:-1] = Xm[1:]  # shift data in the temporal mean 1 sample left
        value = lineread[x]  # read line (single value) from the serial port
        Xm[-1] = float(value)  # vector containing the instantaneous values
        plt = (time.time() - start_time)
        curve[x].setData(Xm)  # set the curve with this data

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

every(delay,update)
### END QtApp ####
pg.QtGui.QApplication.exec_()  # you MUST put this at the end
##################