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
gxs = []
gys = []
gzs = []

list_limit = 30

t = 0
while t < 100:

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

	axs.append(ACCx)
	ays.append(ACCy)
	gxs.append(GYRx)
	gys.append(GYRy)
	gzs.append(GYRz)

	

	if 0:					   #Change to '0' to stop showing the angles from the accelerometer
		outputString += "#  ACCX Angle %5.2f ACCY Angle %5.2f  #  " % (ACCx, ACCy)

	if 0:					   #Change to '0' to stop  showing the angles from the gyro
		outputString +="\t# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (GYRx,GYRy,GYRz)

	#print(outputString)

	#slow program down a bit, makes the output more readable
	time.sleep(0.05)
	t += 1

print("Data collected, writing to data.csv")
np.savetxt('data.csv', (axs,ays,gxs,gys,gzs), delimiter=',')
print("File saved")