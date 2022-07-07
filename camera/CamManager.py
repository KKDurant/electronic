from CameraImport import *
from Camera import Camera
from PIL import Image
import numpy as np
class CamManager():
    def __init__(self) -> None:
        self.deviceList = self.enumDevices()
        noneCam = Camera(None)
        self.cameras = {'left':noneCam,'right':noneCam,'front':noneCam,'behind':noneCam,'top':noneCam}
        pass
    def getDeviceInfo(self, selDeviceInfo):# 解析设备信息
        mvcc_dev_info = cast(selDeviceInfo, POINTER(
            MV_CC_DEVICE_INFO)).contents
        if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
            #print ("\ngige device: [%d]" % i)
            chUserDefinedName = ""
            for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chUserDefinedName:
                if 0 == per:
                    break
                chUserDefinedName = chUserDefinedName + chr(per)
            #print ("device model name: %s" % chUserDefinedName)

            nip1 = (
                (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
            nip2 = (
                (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
            nip3 = (
                (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
            nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
            print("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
            #devList.append("["+str(i)+"]GigE: "+ chUserDefinedName +"("+ str(nip1)+"."+str(nip2)+"."+str(nip3)+"."+str(nip4) +")")
        elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
            #print ("\nu3v device: [%d]" % i)
            chUserDefinedName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chUserDefinedName:
                if per == 0:
                    break
                chUserDefinedName = chUserDefinedName + chr(per)
            #print ("device model name: %s" % chUserDefinedName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            #print ("user serial number: %s" % strSerialNumber)
            #devList.append("["+str(i)+"]USB: "+ chUserDefinedName +"(" + str(strSerialNumber) + ")")
        return
    def enumDevices(self):# 枚举连接到本机的相机
        deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
        if ret != 0:
            print('show error', '枚举设备失败! ret = ' + str(ret))
            return None
        if deviceList.nDeviceNum == 0:
            print('show info', 'find no device!')
            return None
        print("找到 %d 个设备!" % deviceList.nDeviceNum)
        return deviceList
    def openDevice(self, selCamIndex:int)->Camera:# 获取指定相机的对象
        selDevice = cast(self.deviceList.pDeviceInfo[int(
            selCamIndex)], POINTER(MV_CC_DEVICE_INFO)).contents
        camera = Camera(selDevice)
        camera.openDevice()
        return camera
    def setOrientation(self,orientation:str,camera):# 将相机对象与指定方向绑定
        self.cameras[orientation]=camera
    def getOneFrame(self,orientation,timeout=10000)->np.array:# 从指定方向的相机获取一帧图片
        self.cameras[orientation].startGrabbing()
        pic = self.cameras[orientation].getOneFrame(timeout)
        self.cameras[orientation].stopGrabbing()
        return pic

    def setCameraParams(self,orientation:str,param:str,value):
        self.cameras[orientation].setParam(param,value)

    def getCameraParams(self,orientation:str,param:str):
        self.cameras[orientation].getParam(param)

    
if __name__ == "__main__":
    camManager = CamManager()
    print(camManager.deviceList)
    camManager.getDeviceInfo(camManager.deviceList.pDeviceInfo[0])
    camera = camManager.openDevice(0)
    camManager.setOrientation('left',camera)
    #camera.setParam("Width",1280)
    #camera.setParam("Height",854)
    #camera.openDevice()
    #camera.startGrabbing()
    #camera.closeDevice()
    nparray= camManager.getOneFrame('left')
    #camera.stopGrabbing()
    camera.closeDevice()
    img = Image.fromarray(nparray, 'RGB')
    img.show()