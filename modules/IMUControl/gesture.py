import sys
import time
import math
import IMUControl.IMU
import datetime
import os
from MQTT.transmitSong import MQTTTransmitter

import sys

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
transmitterInstance = MQTTTransmitter()

if len(sys.argv) == 2:
    topic = sys.argv[1]
    transmitterInstance.setTopic(topic)

    
def sendIMU(command):
    transmitterInstance.setCommand(command)
    client = transmitterInstance.connect_mqtt()
    client.loop_start()
    transmitterInstance.publish(client)
    client.loop_stop()

def timeset(diffin, com):
    out = 0.35
    if com == 'n' :
        if diffin < 3000 :
            out = 0.4
        elif diffin > 8000:
            out = 0.3
    if com == 'p' :
        if diffin > -3000 :
            out = 0.4
        elif diffin < -8000 :
            out = 0.3
    if com == 't' :
        out = 0.4
        if diffin < 3000 :
            out = 0.45
        elif diffin > 8000:
            out = 0.35
    return out

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

    if diffGYRx > 1800 :    #read clockwise hand motion
        t = timeset(diffGYRx,'n')
        time.sleep(t)            #delay for counter clockwise hand motion        .35
        GYRxTemp = IMUControl.IMU.readGYRx()   #read 
        diffTempn = GYRx - GYRxTemp
        #print(diffTempn, ",", diffGYRx)
        if diffTempn < (diffGYRx*-.9) :     #check for counter clockwise motion
            sendIMU("NEXT")     #the output command for Next Song
            time.sleep(0.3)
    if diffGYRx < -2000 :
        t = timeset(diffGYRx,'p')
        time.sleep(t)            #delay for counter clockwise hand motion        .35
        GYRxTemp = IMUControl.IMU.readGYRx()   #read 
        diffTempp = GYRx - GYRxTemp
        #print(diffTempp, ",", diffGYRx)
        if diffTempp > (diffGYRx*-.9) :     #check for counter clockwise motion
            sendIMU("PREV")     #the output command for Previous Song
            time.sleep(0.3)
    if diffGYRz > 2000 :
        t = timeset(diffGYRx,'t')
        time.sleep(t)
        GYRzTemp = IMUControl.IMU.readGYRz()
        diffTemps = GYRz - GYRzTemp
        #print(diffTemps, ",", diffGYRz)
        if diffTemps < (diffGYRz*-.9) :
            sendIMU("TOGGLE")      #the output command for play and pause
            time.sleep(0.3)

    pastGYRx = GYRx

    time.sleep(0.2)
