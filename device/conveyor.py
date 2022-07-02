import sys,os
from time import sleep
from tkinter.tix import Tree
sys.path.append(os.getcwd())
from communicate import plcCommunicate

class Conveyor():
    def __init__(self,plc:plcCommunicate.S7_200Smart_PLC) -> None:
        self.plc= plc
        pass
    def run(self,speed=20):# 开机
        self.setSpeed(speed)
        byte_array= self.plc.readM(0)
        #print(byte_array)
        self.plc.setBit(byte_array,0)
        #print(byte_array)
        self.plc.writeM(0,byte_array)
        pass
    def stop(self):# 停机
        byte_array= self.plc.readM(0)
        #print(byte_array)
        self.plc.setBit(byte_array,0,False)
        #print(byte_array)
        #while True:
        self.plc.writeM(0,byte_array)
        pass
    def getSpeed(self) -> float:#获取传送带速度
        speed = self.plc.byteArrayToData(self.plc.readVD(200),'real')
        return speed
    def setSpeed(self,speed):#设置传送带速度
        self.plc.writeVD(200,self.plc.dataToByteArray(speed,'real'))

class PhotoelectricSensor():
    def __init__(self,plc:plcCommunicate.S7_200Smart_PLC) -> None:
        self.plc= plc
        self.oldStatus = False
        self.newStatus = False
        pass
    def objInArea(self):# 是否有物体在拍摄区域
        plcI1=self.plc.readI(1)
        return 0 == self.plc.getBit(plcI1,6)
    def arrive(self) -> bool:# 物体到达
        self.newStatus= self.objInArea()
        if (True==self.newStatus) and (False==self.oldStatus):
            self.oldStatus=self.newStatus
            return True
        else:
            self.oldStatus=self.newStatus
            return False

    # #获取传送带速度
    # def getSpeed(self) -> float:
    #     speed = self.plc.getSpeed()
    #     return speed
    # #设置传送带速度
    # def setSpeed(self,speed):
    #    self.plc.setSpeed(speed)

if __name__ == '__main__':
    plc= plcCommunicate.S7_200Smart_PLC()
    plc.connect_200smart("192.168.3.50")
    if plc.get_connected():
        print(1)
        conveyor = Conveyor(plc)
        #conveyor.run()
        #sleep(3)
        conveyor.stop()
        conveyor.run(50)