import sys
import time
import math
import IMU
import datetime
import os

### IMPORTANT ###
#Make sure that this file location is put into the directory below
#pi/BerryIMU/python-BerryIMU-gyro-accel-compass-filters

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070          # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40              # Complementary filter constant
MAG_LPF_FACTOR = 0.4    # Low pass filter constant magnetometer
ACC_LPF_FACTOR = 0.4    # Low pass filter constant for accelerometer
ACC_MEDIANTABLESIZE = 9         # Median filter table size for accelerometer. Higher = smoother but a longer delay
MAG_MEDIANTABLESIZE = 9         # Median filter table size for magnetometer. Higher = smoother but a longer delay
ACCxpast = 0
ACCzpast = 0

################# Compass Calibration values ############
# Use calibrateBerryIMU.py to get calibration values
# Calibrating the compass isnt mandatory, however a calibrated
# compass will result in a more accurate heading value.

magXmin =  -2372
magYmin =  -4110
magZmin =  4386
magXmax =  -1643
magYmax =  -1303
magZmax =  4506


'''
Here is an example:
magXmin =  -1748
magYmin =  -1025
magZmin =  -1876
magXmax =  959
magYmax =  1651
magZmax =  708
Dont use the above values, these are just an example.
'''
############### END Calibration offsets #################


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

gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0
CFangleXFiltered = 0.0
CFangleYFiltered = 0.0
kalmanX = 0.0
kalmanY = 0.0
oldXMagRawValue = 0
oldYMagRawValue = 0
oldZMagRawValue = 0
oldXAccRawValue = 0
oldYAccRawValue = 0
oldZAccRawValue = 0

a = datetime.datetime.now()



#Setup the tables for the mdeian filter. Fill them all with '1' so we dont get devide by zero error
acc_medianTable1X = [1] * ACC_MEDIANTABLESIZE
acc_medianTable1Y = [1] * ACC_MEDIANTABLESIZE
acc_medianTable1Z = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2X = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2Y = [1] * ACC_MEDIANTABLESIZE
acc_medianTable2Z = [1] * ACC_MEDIANTABLESIZE
mag_medianTable1X = [1] * MAG_MEDIANTABLESIZE
mag_medianTable1Y = [1] * MAG_MEDIANTABLESIZE
mag_medianTable1Z = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2X = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2Y = [1] * MAG_MEDIANTABLESIZE
mag_medianTable2Z = [1] * MAG_MEDIANTABLESIZE

IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

pastGYRx = 0
pastGYRz = 0
count = 0
command = 0

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


    #Apply compass calibration
    MAGx -= (magXmin + magXmax) /2
    MAGy -= (magYmin + magYmax) /2
    MAGz -= (magZmin + magZmax) /2


    ##Calculate loop Period(LP). How long between Gyro Reads
    b = datetime.datetime.now() - a
    a = datetime.datetime.now()
    LP = b.microseconds/(1000000*1.0)
    outputString = "Loop Time %5.2f " % ( LP )


    ##################### END Tilt Compensation ########################

    #print(IMU.readACCx(),IMU.readACCy(),IMU.readACCz())
    #print(IMU.readGYRx(), IMU.readGYRy(), IMU.readGYRz())

    diffGYRx = pastGYRx - GYRx
    diffGYRz = pastGYRz - GYRz
    print(diffGYRx)

    if command != 0 :
        command = 0

    if diffGYRx > 1000 :    #read clockwise hand motion
        time.sleep(0.15)            #delay for counter clockwise hand motion
        GYRxTemp = IMU.readGYRx()   #read 
        diffTemp = GYRx - GYRxTemp
        print("p2")
        print(diffTemp)
        if diffTemp < -1000 :     #check for counter clockwise motion
            print("Next Song")
            command = 3
            time.sleep(1.1)
    if diffGYRx < -1000 : 
        time.sleep(0.15)            #delay for counter clockwise hand motion
        GYRxTemp = IMU.readGYRx()   #read 
        diffTemp = GYRx - GYRxTemp
        if diffTemp > 1500 :     #check for counter clockwise motion
            print("Previous Song")
            command = 4
            time.sleep(1.1)
    #if diffGYRz > 1000 :
    #    print("Play Song")
    #    command = 1
    #    time.sleep(1)


    pastGYRx = GYRx

    time.sleep(0.2)


    #needs files from the berry.IMU that i will post later