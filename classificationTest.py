# motionClassifierTest.py
# Simple classifier to differentiate between forward push (Y) and upward lift (Z)

import sys
import time
import math
import IMU
import datetime
import os
import numpy as np
import csv

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


axs = []
ays = []
azs = []
gxs = []
gys = []
gzs = []

# Thresholds
# Vertical
z_th_up = 6000
z_th_down = 2500

# Side to side
x_th_right = 2000
x_th_left = -2500

# Front back (likely not used)
y_th_front = 2000
y_th_back = -1000

t = 0
# one minute: 1200
while True:

	#Read the accelerometer,gyroscope and magnetometer values
	ACCx = IMU.readACCx()
	ACCy = IMU.readACCy()
	ACCz = IMU.readACCz()
	GYRx = IMU.readGYRx()
	GYRy = IMU.readGYRy()
	GYRz = IMU.readGYRz()
	MAGx = IMU.readMAGx()
	MAGy = IMU.readMAGy()
	MAGz = IMU.readMAGz()

	#axs.append(ACCx)
	#ays.append(ACCy)
	#azs.append(ACCz)
	#gxs.append(GYRx)
	#gys.append(GYRy)
	#gzs.append(GYRz)

	# Vertical classification
	if ACCz > z_th_up:
		print("Up!")
	elif ACCz < z_th_down:
		print("Down!")

	# Left right classification
	if ACCx > x_th_right:
		print("Right!")
	elif ACCx < x_th_left:
		print("Left!")

	# Front back classification
	if ACCy > y_th_front:
		print("Forward!")
	elif ACCy < y_th_back:
		print("Back!")
	

	#slow program down a bit, makes the output more readable
	time.sleep(0.05)
	t += 1
