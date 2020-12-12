import sys
import time
import math
import IMUControl.IMU
import datetime
import os
from MQTT.transmitSong import MQTTTransmitter

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

magXmin =  -2372
magYmin =  -4110
magZmin =  4386
magXmax =  -1643
magYmax =  -1303
magZmax =  4506


a = datetime.datetime.now()

IMUControl.IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMUControl.IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMUControl.IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

pastGYRx = 0
pastGYRz = 0
count = 0
command = "NONE"
transmitterInstance = MQTTTransmitter()

    
def sendIMU(command):
    transmitterInstance.setCommand(command)
    client = transmitterInstance.connect_mqtt()
    client.loop_start()
    transmitterInstance.publish(client)
    client.loop_stop()

while True:

    #Read the accelerometer,gyroscope and magnetometer values
    #ACCx = IMU.readACCx()
    #ACCy = IMU.readACCy()
    #ACCz = IMU.readACCz()
    GYRx = IMUControl.IMU.readGYRx()
    GYRy = IMUControl.IMU.readGYRy()
    GYRz = IMUControl.IMU.readGYRz()

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
        #print(command)

    if diffGYRx > 1800 :    #read clockwise hand motion
        time.sleep(0.35)            #delay for counter clockwise hand motion        .35
        GYRxTemp = IMUControl.IMU.readGYRx()   #read 
        diffTempn = GYRx - GYRxTemp
        if diffTempn < -5000 :     #check for counter clockwise motion
            command = "NEXT"             #the output command for Next Song
            #print(command)
            sendIMU(command)
            time.sleep(.9)
    if diffGYRx < -2000 :
        time.sleep(0.35)            #delay for counter clockwise hand motion        .35
        GYRxTemp = IMUControl.IMU.readGYRx()   #read 
        diffTempp = GYRx - GYRxTemp
        if diffTempp > 4500 :     #check for counter clockwise motion
            command = "PREV"             #the output command for Previous Song
            #print(command)
            sendIMU(command)
            time.sleep(.9)
    if diffGYRz > 2000 :
        time.sleep(0.4)
        GYRzTemp = IMUControl.IMU.readGYRz()
        diffTemps = GYRz - GYRzTemp
        if diffTemps < -5000 :
            command = "TOGGLE"      #the output command for play and pause
            print(command)
            sendIMU(command)
            time.sleep(.9)

    pastGYRx = GYRx

    time.sleep(0.2)

