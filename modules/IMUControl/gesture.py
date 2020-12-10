import sys
import time
import math
import IMU
import datetime
import os
import json

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

a = datetime.datetime.now()

IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

pastGYRx = 0
pastGYRz = 0
count = 0
command = "NONE"
out = json.dumps(command)

while True:

    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()
    GYRx = IMU.readGYRx()
    GYRy = IMU.readGYRy()
    GYRz = IMU.readGYRz()
    #MAGx = IMU.readMAGx()
    #MAGy = IMU.readMAGy()
    #MAGz = IMU.readMAGz()

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
    #print(diffGYRx)

    if command != "NONE" :
        command = "NONE"
        with open("IMUCommand.json", "w") as write_file:
                json.dump(command, write_file)

    if diffGYRx > 1800 :    #read clockwise hand motion
        #print(diffGYRx)
        time.sleep(0.35)            #delay for counter clockwise hand motion        .35
        GYRxTemp = IMU.readGYRx()   #read 
        diffTempn = GYRx - GYRxTemp
        #print(diffTemp)
        if diffTempn < -5000 :     #check for counter clockwise motion
            #print("Next Song")
            command = "NEXT"             #the output command for Next Song
            with open("IMUCommand.json", "w") as write_file:
                json.dump(command, write_file)
            #print(command)
            time.sleep(.9)
    if diffGYRx < -2000 :
        #print(diffGYRx)
        time.sleep(0.35)            #delay for counter clockwise hand motion        .35
        GYRxTemp = IMU.readGYRx()   #read 
        diffTempp = GYRx - GYRxTemp
        #print(diffTempp)
        if diffTempp > 4500 :     #check for counter clockwise motion
            #print("Previous Song")
            command = "PREV"             #the output command for Previous Song
            #print(command)
            with open("IMUCommand.json", "w") as write_file:
                json.dump(command, write_file)
            time.sleep(.9)
    if diffGYRz > 2000 :
        #print(diffGYRz)
        time.sleep(0.4)
        GYRzTemp = IMU.readGYRz()
        #print(GYRzTemp)
        diffTemps = GYRz - GYRzTemp
        #print(diffTemp)
        if diffTemps < -5000 :
            #print("Play Song/Pause Song")
            command = "TOGGLE"      #the output command for play and pause
            #print(command)
            with open("IMUCommand.json", "w") as write_file:
                json.dump(command, write_file)
            time.sleep(.9)

    pastGYRx = GYRx

    time.sleep(0.2)

