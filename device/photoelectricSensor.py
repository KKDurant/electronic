import sys,os
sys.path.append(os.getcwd())
#print(sys.path)
from communicate import plcCommunicate

# class PhotoelectricSensor():
#     def __init__(self,plc:plcCommunicate.PESensorCom) -> None:
#         self.plc= plc
#         self.oldStatus = False
#         self.newStatus = False
#         pass
        
#     def arrive2(self) -> bool:
#         plcI1=self.plc.readI(1)
#         self.newStatus= self.plc.getBit(plcI1,6)
#         if (0==self.newStatus) and (1==self.oldStatus):
#             self.oldStatus=self.newStatus
#             return True
#         else:
#             self.oldStatus=self.newStatus
#             return False
    
#     def arrive(self) -> bool:
#         self.newStatus= self.plc.objInArea()
#         if (True==self.newStatus) and (False==self.oldStatus):
#             self.oldStatus=self.newStatus
#             return True
#         else:
#             self.oldStatus=self.newStatus
#             return False

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


if __name__ == '__main__':
    plc= plcCommunicate.S7_200Smart_PLC()
    plc.connect_200smart("192.168.3.50")
    peSensor = PhotoelectricSensor(plc)
    while True:
        print(peSensor.objInArea())
    # if plc.get_connected():
    #     peSensor = PhotoelectricSensor(plc)
    #     while True:
    #         if peSensor.arrive():
    #             print(True)
            