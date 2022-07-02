import json
import sys
from time import sleep

from communicate import S7_200Smart_PLC
from device import PhotoelectricSensor


def detectProductPosition(re,severThreading):
    plc_listen = S7_200Smart_PLC()
    plc_listen.connect_200smart("192.168.3.50")
    peSensor = PhotoelectricSensor(plc_listen)
    while True:
        if peSensor.objInArea():
            re['content'] = 'True'
            print(re)
        else:
            re['content'] = 'False'
            print(re)
        severThreading.sendMessage(re)