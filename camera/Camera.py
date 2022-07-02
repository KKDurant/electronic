
from CameraImport import *
import camUtil as camUtil
import time
from ctypes import *

class Camera:
    def __init__(self, selDevice) -> None:# 初始化
        # openDevice()
        self.device = selDevice
        pass
    def openDevice(self):# 打开设备
        self.obj_cam = MvCamera()
        ret = self.obj_cam.MV_CC_CreateHandle(self.device)
        if ret != 0:
            self.obj_cam.MV_CC_DestroyHandle()
            print("show error", "create handle fail! ret = " + self.To_hex_str(ret))
            return ret
        ret = self.obj_cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
        if ret != 0:
            print("show error", "open device fail! ret = " + self.To_hex_str(ret))
            return ret
        print("open device successfully!")
        self.optimizePackageSize()
        # 获取帧率设定
        stBool = c_bool(False)
        ret = self.obj_cam.MV_CC_GetBoolValue("AcquisitionFrameRateEnable", stBool)
        if ret != 0:
            print("get acquisition frame rate enable fail! ret[0x%x]" % ret)
        # 设置触发模式为off
        self.setTriggerMode(False)
        return 0
    def closeDevice(self):#关闭设备
        # 退出线程
        ret = self.obj_cam.MV_CC_CloseDevice()
        if ret != 0:
            print("show error", "close deivce fail! ret = " + str(ret))
            return
        # 销毁句柄
        self.obj_cam.MV_CC_DestroyHandle()
        print("close device successfully!")
    def startGrabbing(self):# 开始抓取图像
        ret = self.obj_cam.MV_CC_StartGrabbing()
        if ret != 0:
            print("show error", "start grabbing fail! ret = " + self.To_hex_str(ret))
            return
        print("start grabbing successfully!")
    def getOneFrame(self,timout=10000):# 获得一帧图像
        stOutFrame = MV_FRAME_OUT()
        img_buff = None
        buf_cache = None
        numArray = None
        ret = self.obj_cam.MV_CC_GetImageBuffer(stOutFrame, timout)
        if 0 == ret:
            if None == buf_cache:
                buf_cache = (c_ubyte * stOutFrame.stFrameInfo.nFrameLen)()
            # 获取到图像的时间开始节点获取到图像的时间开始节点
            self.st_frame_info = stOutFrame.stFrameInfo
            cdll.msvcrt.memcpy(
                byref(buf_cache), stOutFrame.pBufAddr, self.st_frame_info.nFrameLen
            )
            print(
                "get one frame: Width[%d], Height[%d], nFrameNum[%d]"
                % (
                    self.st_frame_info.nWidth,
                    self.st_frame_info.nHeight,
                    self.st_frame_info.nFrameNum,
                )
            )
            self.n_save_image_size = (
                self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3 + 2048
            )
            if img_buff is None:
                img_buff = (c_ubyte * self.n_save_image_size)()
        else:
            print("no data, nret = " + self.To_hex_str(ret))
            return None
        # 转换像素结构体赋值
        stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
        memset(byref(stConvertParam), 0, sizeof(stConvertParam))
        stConvertParam.nWidth = self.st_frame_info.nWidth
        stConvertParam.nHeight = self.st_frame_info.nHeight
        stConvertParam.pSrcData = cast(buf_cache, POINTER(c_ubyte))
        stConvertParam.nSrcDataLen = self.st_frame_info.nFrameLen
        stConvertParam.enSrcPixelType = self.st_frame_info.enPixelType
        # RGB直接显示
        if PixelType_Gvsp_RGB8_Packed == self.st_frame_info.enPixelType:
            numArray = camUtil.Color_numpy(
                buf_cache, self.st_frame_info.nWidth, self.st_frame_info.nHeight
            )

        # 如果是彩色且非RGB则转为RGB后显示
        else:
            nConvertSize = self.st_frame_info.nWidth * self.st_frame_info.nHeight * 3
            stConvertParam.enDstPixelType = PixelType_Gvsp_RGB8_Packed
            stConvertParam.pDstBuffer = (c_ubyte * nConvertSize)()
            stConvertParam.nDstBufferSize = nConvertSize
            time_start = time.time()
            ret = self.obj_cam.MV_CC_ConvertPixelType(stConvertParam)
            time_end = time.time()
            print("MV_CC_ConvertPixelType:", time_end - time_start)
            if ret != 0:
                print("show error", "convert pixel fail! ret = " + self.To_hex_str(ret))
                return None
            cdll.msvcrt.memcpy(byref(img_buff), stConvertParam.pDstBuffer, nConvertSize)
            numArray = camUtil.Color_numpy(
                img_buff, self.st_frame_info.nWidth, self.st_frame_info.nHeight
            )
        nRet = self.obj_cam.MV_CC_FreeImageBuffer(stOutFrame)
        return numArray
    def stopGrabbing(self):# 停止抓取
        ret = self.obj_cam.MV_CC_StopGrabbing()
        if ret != 0:
            print("show error", "stop grabbing fail! ret = " + self.To_hex_str(ret))
            return
        print("stop grabbing successfully!")
    def getParam(self,param:str):# 获得相机参数
        result=None
        # 获得整型参数
        if param in ("Width", "Height"):
            value = MVCC_INTVALUE()
            memset(byref(value), 0, sizeof(MVCC_INTVALUE))
            ret = self.obj_cam.MV_CC_GetIntValue(param, value)
            if ret != 0:
                print(
                    "show error",
                    "get "+ param + " fail! ret = " + self.To_hex_str(ret),
                )
            else:
                result= value.nCurValue
        # 获得浮点型参数
        elif param in ("AcquisitionFrameRate","ExposureTime"):
            value = MVCC_FLOATVALUE()
            memset(byref(value), 0, sizeof(MVCC_FLOATVALUE))
            ret = self.obj_cam.MV_CC_GetFloatValue(param, value)
            if ret != 0:
                print(
                    "show error",
                    "get "+ param + " fail! ret = " + self.To_hex_str(ret),
                )
            else:
                result= value.fCurValue
        else:
            print(param + "参数的获取尚未实现，请检查参数名")
        return result
    def setParam(self,param:str,value):# 设置相机参数
        ret=0
        # 设置整型参数
        if param in ("Width", "Height"):
            ret = self.obj_cam.MV_CC_SetIntValue(param, value)
            if ret != 0:
                print(
                    "show error",
                    "set "+ param + " fail! ret = " + self.To_hex_str(ret),
                )
        # 设置浮点型参数
        elif param in ("AcquisitionFrameRate","ExposureTime"):
            ret = self.obj_cam.MV_CC_SetFloatValue(param, value)
            if ret != 0:
                print(
                    "show error",
                    "set "+ param + " fail! ret = " + self.To_hex_str(ret),
                )
        else:
            print(param + "参数的设置尚未实现，请检查参数名")
        return ret    
    def To_hex_str(self, num):# 十六进制显示转换
        chaDic = {10: "a", 11: "b", 12: "c", 13: "d", 14: "e", 15: "f"}
        hexStr = ""
        if num < 0:
            num = num + 2 ** 32
        while num >= 16:
            digit = num % 16
            hexStr = chaDic.get(digit, str(digit)) + hexStr
            num //= 16
        hexStr = chaDic.get(num, str(num)) + hexStr
        return hexStr
    def setTriggerMode(self, bool=False):# 设置触发模式
        ret = 0
        if bool == True:
            ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_ON)
        elif bool == False:
            ret = self.obj_cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
        if ret != 0:
            print("set trigger mode fail! ret[0x%x]" % ret)
        return ret
    def optimizePackageSize(self):# 优化网络包大小
        if self.device.nTLayerType == MV_GIGE_DEVICE:
            nPacketSize = self.obj_cam.MV_CC_GetOptimalPacketSize()
            if int(nPacketSize) > 0:
                ret = self.obj_cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
                if ret != 0:
                    print("warning: set packet size fail! ret[0x%x]" % ret)
            else:
                print("warning: set packet size fail! ret[0x%x]" % nPacketSize)

if __name__ == "__main__":
    pass
