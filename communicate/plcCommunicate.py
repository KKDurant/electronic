
from random import random
from typing import Optional
from nbformat import read

import snap7
from snap7 import util, client
import random

from time import sleep

class S7_200Smart_PLC(client.Client):
    def __init__(self, lib_location: Optional[str] = None):
        client.Client.__init__(self,lib_location)
    def connect_200smart(self,ip: str, plc_model=3, rack=0, slot=1):
        """
            连接s7-200smart系列
        :param ip: PLC/设备IPV4地址
        :param plc_model: 连接类型：1用于PG，2用于OP，3至10用于S7基本
        :param rack: 服务器上的机架
        :param slot: 服务器上的插槽
        """
        # 设置连接资源类型，即客户端,连接到PLC
        self.set_connection_type(plc_model)
        # 连接到S7服务器
        self.connect(ip, rack, slot)
    def byteArrayToData(self,byte_array,datatype):#bytearray数据转换为制定格式数据
        if datatype == 'real':
            return util.get_real(byte_array,0)
        elif datatype == 'dint':
            return util.get_dint(byte_array,0)
        elif datatype == 'dword':
            return util.get_dword(byte_array,0)
        elif datatype == 'dt':
            return util.get_dt(byte_array,0)
        elif datatype == 'usint':
            return util.get_usint(byte_array,0)
        else:
            print("datatype not implemented!")    
    def dataToByteArray(self,data,datatype):#指定格式数据转换为bytearray数据
        if datatype == 'real':
            return util.set_real(bytearray(4),0,data)
        elif datatype == 'dint':
            return util.get_dint(bytearray(4),0,data)
        elif datatype == 'dword':
            return util.get_dword(bytearray(4),0,data)
        elif datatype == 'dt':
            return util.get_dt(bytearray(4),0,data)
        elif datatype == 'usint':
            return util.get_usint(bytearray(4),0,data)
        else:
            print("datatype not implemented!")
    def readI(self,offset):#读取I
        byte_array= self.read_area(snap7.types.Areas.PE, 0, offset, 4)
        return byte_array
    def writeI(self,offset:int,byte_array:bytearray):#写入I
        self.write_area(snap7.types.Areas.PE, 0, offset, byte_array)
    def readVD(self,offset):#读取VD
        byte_array= self.read_area(snap7.types.Areas.DB, 1, offset, 4)
        return byte_array
    def writeVD(self,offset:int,byte_array:bytearray):#写入VD
        self.write_area(snap7.types.Areas.DB, 1, offset, byte_array)
    def readM(self,offset:int):#读取M
        byte_array=self.read_area(snap7.types.Areas.MK, 0, offset, 1)
        return byte_array
    def writeM(self,offset:int,byte_array:bytearray):#写入M
        self.write_area(snap7.types.Areas.MK, 0, offset, byte_array)
    def getBit(self,byte_array:bytearray,bit:int):#读取一个字节的某一个位
        return (util.get_byte(byte_array,0)>>bit)&1
    def setBit(self,byte_array:bytearray,bit:int,value:bool=True):#设置一个字节的某个bit位
        originByte=util.get_byte(byte_array,0)
        if value:
            return util.set_byte(byte_array,0,originByte|(1<<bit))
        else:
            return util.set_byte(byte_array,0,originByte&(~(1<<bit)))
    def readQ(self,offset:int):#读取Q区
        byte_array=self.read_area(snap7.types.Areas.PA, 0, offset, 1)
        return byte_array
    def __del__(self):
        pass 

class PESensorCom(S7_200Smart_PLC):
    # 物体是否在传感器检测区域，是返回True，否Fan返回False
    def objInArea(self) -> bool:
        plcI1=self.readI(1)
        return 0 == self.getBit(plcI1,6)

class ConveyorCom(S7_200Smart_PLC):
    # 开机
    def run(self,speed=200):
        self.setSpeed(200)
        pass
    
    # 停机
    def stop(self):
        pass

    #获取传送带速度
    def getSpeed(self) -> float:
        speed = self.byteArrayToData(self.readVD(200),'real')
        return speed

    #设置传送带速度
    def setSpeed(self,speed):
        self.writeVD(200,self.dataToByteArray(speed,'real'))

if __name__ == '__main__':
    plc= S7_200Smart_PLC()
    plc.connect_200smart("192.168.3.50")
    print(plc.get_connected())
    while True:
        print(plc.readI(1))
    # print("M2改变前",end=' ')
    # byte_array= plc.readM(2)
    # print(byte_array)
    # #设置M2.2 M2.5 M2.7为1
    # plc.setBit(byte_array,2)
    # plc.setBit(byte_array,5)
    # plc.setBit(byte_array,7)
    # print(byte_array)
    # plc.writeM(2,byte_array)
    # print("M2改变后",end=' ')
    # print(plc.readM(2))
    print("VD200改变前",end=' ')
    print(plc.byteArrayToData(plc.readVD(200),'real'))
    # plc.writeVD(200,plc.dataToByteArray(20.0,'real'))
    # print("VD200改变后",end=' ')
    # print(plc.byteArrayToData(plc.readVD(200),'real'))
    #print(plc.setBit(byte_array,7,True))
    plc.disconnect()
    plc.destroy()
    # plc= PESensorCom()
    # plc.connect_200smart("192.168.3.50")
    # while True:
    #     print(plc.objInArea())