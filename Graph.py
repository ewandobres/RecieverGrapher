# Import libraries
from itertools import cycle
from random import randrange, uniform
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time


start_time = time.time()
delay = .5

# Create object serial port
portName = "COM12"  # replace this port name by yours!
baudrate = 9600
# ser = serial.Serial(portName, baudrate)

sensornum = 2
curve = []
### START QtApp #####
app = QtGui.QApplication([])  # you MUST do this once (initialize things)

win = pg.GraphicsWindow(title="Signal from serial port")  # creates a window

for x in range(sensornum):
    p = win.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
    curve.append(p.plot())  # create an empty "plot" (a curve to plot)

windowWidth = 10  # width of the window displaying the curve

# Xm = linspace(0, 0, windowWidth)  # create array that will contain the relevant time series
ptr = -windowWidth  # set first x position
dataArray = np.linspace(0, 0, windowWidth)
timesense = []
loopnum = 0
sensor = []
lines = []

#f = open("testdata.txt")

#for x in f:
#    lines.append(x)


#f.close()
#pool = cycle(lines)

pltcount = 0


# Realtime data plot. Each time this function is called, the data display is updated
def update():

    lineread = []

    #arduinoData = next(pool)

    #lineread = (arduinoData.split(','))



    for x in range(sensornum):
       lineread.append(uniform(0, 100))

    outfile = open("output.csv", "a")
    for x in range(sensornum):
        if x == sensornum -1:
            outfile.write(str(round(lineread[x] , 2)))
        else:
            outfile.write(str(round(lineread[x] , 2)) + ",")

    outfile.write("\n")
    outfile.close()
    #
    for x in range(sensornum):
        global curve, ptr, dataArray
        value = []
        plt = []

        for y in range(sensornum):
            newarray = []
            value.append(float(lineread[y]))  # read line (single value) from the serial port
            dataArray = np.append(dataArray, value[y])
            dataArray = np.delete(dataArray, 0)
            plt = (time.time() - start_time) / delay - windowWidth  # update x position for displaying the curve
            curve[x].setData(dataArray)  # set the curve with this data
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
