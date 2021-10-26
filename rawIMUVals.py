# motionClassifierTest.py
# Simple classifier to differentiate between forward push (Y) and upward lift (Z)

import sys
import time
import math
import IMU
import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070		  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40			  # Complementary filter constant
MAG_LPF_FACTOR = 0.4	# Low pass filter constant magnetometer
ACC_LPF_FACTOR = 0.4	# Low pass filter constant for accelerometer
ACC_MEDIANTABLESIZE = 9		 # Median filter table size for accelerometer. Higher = smoother but a longer delay
MAG_MEDIANTABLESIZE = 9		 # Median filter table size for magnetometer. Higher = smoother but a longer delay


# Compass Calibration offset
# Values found by running calibrateBerryIMU.py
magXmin =  -22661
magYmin =  32736
magZmin =  3873
magXmax =  -22584
magYmax =  32767
magZmax =  4260

#Kalman filter variables
Q_angle = 0.02
Q_gyro = 0.0015
R_angle = 0.005
y_bias = 0.0
x_bias = 0.0
XP_00 = 0.0
XP_01 = 0.0
XP_10 = 0.0
XP_11 = 0.0
YP_00 = 0.0
YP_01 = 0.0
YP_10 = 0.0
YP_11 = 0.0
KFangleX = 0.0
KFangleY = 0.0


a = datetime.datetime.now()

IMU.detectIMU()	 #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
	print(" No BerryIMU found... exiting ")
	sys.exit()
IMU.initIMU()	   #Initialise the accelerometer, gyroscope and compass


# Live plot code
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
gxs = []
gys = []

list_limit = 30


def animate(i, gxs, gys):
	GYRx = IMU.readGYRx()
	GYRy = IMU.readGYRy()

	gxs.append(GYRx)
	gys.append(GYRy)

	# Limit x and y lists to 20 items
	gxs = gxs[-20:]
	gys = gys[-20:]

	# Draw x and y lists
	ax.clear()
	ax.plot(gxs)
	ax.plot(gys)

	plt.title("Gyroscope values over time")
	plt.ylabel("Gyro value (raw)")


#while True:

	#Read the accelerometer,gyroscope and magnetometer values

ani = animation.FuncAnimation(fig,animate,fargs=(gxs,gys),interval = 1000)
plt.show()

	#slow program down a bit, makes the output more readable
