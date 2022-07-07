import os
import random
import socket
import sys
import threading
from turtle import right
import PySide6.QtWidgets
from threading import Thread
import numpy as np
from pathlib import Path
from time import sleep
import cv2
import matplotlib

from pip import main
from regex import E

from SocketCommunication.JavaImageConnect import SendImageThread
from camera import CamManager
from detectionModel import YoloModel
from communicate.plcCommunicate import S7_200Smart_PLC,PESensorCom,ConveyorCom
from device import *
from queue import Queue
from PIL import Image, ImageTk
from PySide6.QtGui import QImage,QPixmap
from PySide6.QtWidgets import QApplication,QMainWindow,QComboBox
from PySide6.QtUiTools import QUiLoader
from device.photoelectricSensor import PhotoelectricSensor

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # 根目录
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # 把根目录加到PATH中
CONFIGPATH = Path(os.path.join("detectionModel"))

class MainWindowLogic():
    def __init__(self) -> None:# 初始化
        # self.ui = ui
        # 加载相机管理
        self.camManager = CamManager()
        self.camera = self.openCamera()
        # 加载模型
        self.yoloModel=YoloModel(CONFIGPATH/"bestm_tr.pt",CONFIGPATH/"LEDDetection_m_tr.yaml")
        # 创建与S7-200的链接，每个线程创建一个链接（否则运行时会因为不同线程之间的资源竞争而出错）
        self.plc_watchdog= S7_200Smart_PLC()
        self.plc_listen= S7_200Smart_PLC()
        self.plc_docheck= S7_200Smart_PLC()
        # 传送带对象
        self.conveyor = Conveyor(self.plc_watchdog)
        self.connected = False
        # 光纤传感器对象
        self.peSensor= PhotoelectricSensor(self.plc_listen)
        self.connectToPLC()

    # 创建与PLC的链接
    def connectToPLC(self,ip:str="192.168.3.50")->bool:#连接PLC
        self.plc_watchdog.connect_200smart(ip)
        self.plc_listen.connect_200smart(ip)
        self.plc_docheck.connect_200smart(ip)
        # self.conveycom.connect_200smart(ip)
        self.connected= self.plc_watchdog.get_connected() and self.plc_listen.get_connected() and self.plc_docheck.get_connected() #and self.conveycom.get_connected()
        if not self.connected:
            print("Not connected!")
        return self.connected
    def startup(self):# 开始运行
        self.conveyor.run(80)
        
    def stop(self):# 停止运行
        self.conveyor.stop()
        
    def listen(self):#数码管到达监听
        # tDoCheck = None
        # print('start listen')
        # self.count=0
        while True:
            if self.peSensor.arrive():
            #如果读取到对应信号则
                print('arrive')
                # 向java发arrive消息
                # self.conveyor.stop()
                # print('stop')
                # sleep(1.5)
                # tDoCheck = Thread(target=self.doCheck,args=())
                # tDoCheck.start()
                sendImage = SendImageThread()
                print(111111111111111111111111111)
                detect = threading.Thread(target=sendImage.connect, args=(self.yoloModel,self.camera,))
                detect.start()
                sleep(1)
                # sleep(0.5)
                # self.conveyor.run(80)


    def doCheck(self):#对应收到信号后获取图像并拍照检查
        print('check')
        self.openCamera()
        # 从指定方向拍摄一帧
        nparray= self.camManager.getOneFrame('left')
        # 关闭相机
        # camera.closeDevice()
        # 图像格式转换，从RGB转为BGR
        imgBGR = cv2.cvtColor(nparray,cv2.COLOR_RGB2BGR)
        hight=imgBGR.shape[0]
        width=imgBGR.shape[1]
        # 将图像裁剪为左右两部分
        left= imgBGR[0:hight,0:int(0.5*width)]
        right= imgBGR[0:hight,int(0.5*width):width]
        # 两部分分别都进行判断，图像结果存在im_中，json结果存在dict中
        iml,content_dictl=self.yoloModel.run(left)
        imr,content_dictr=self.yoloModel.run(right)
        # 将结果图像拼接
        im0=cv2.hconcat([iml,imr])
        # 图像格式转换，用于显示
        cvRGBImg = cv2.cvtColor(im0,cv2.COLOR_RGB2BGR)
        tmpimg= QImage(cvRGBImg.data,cvRGBImg.shape[1], cvRGBImg.shape[0],QImage.Format_RGB888)
        pixmapImg = QPixmap.fromImage(tmpimg).scaled(1366,288)
        # self.ui.label_img1.setPixmap(pixmapImg)
        # 根据json结果调整ui中的显示

        # glue_det=False
        # pin_glue_det=False
        # pin_inclined_det=False
        # for pred in content_dictl:
        #     if pred["category"].split()[0]=="glue" or pred["category"].split()[0]=="glue_dots":
        #         glue_det=True
        #     if pred["category"].split()[0]=="pin_glue":
        #         pin_glue_det=True
        #     # 我训练模型时拼错了，应该是pin_inclined，重新训练时候改一下训练文件，把这也得改了
        #     if pred["category"].split()[0]=="pin_incliend":
        #         pin_inclined_det=True
        #     pass
        # for pred in content_dictr:
        #     if pred["category"].split()[0]=="glue" or pred["category"].split()[0]=="glue_dots":
        #         glue_det=True
        #     if pred["category"].split()[0]=="pin_glue":
        #         pin_glue_det=True
        #     # 我训练模型时拼错了，应该是pin_inclined，重新训练时候改一下训练文件，把这也得改了
        #     if pred["category"].split()[0]=="pin_incliend":
        #         pin_inclined_det=True
        #     pass
    #     #self.ui.label_img1.show()
    #     # self.setBarColor(self.ui.label_glue,'green')
    #     # self.setBarColor(self.ui.label_pin_glue,'green')
    #     # self.setBarColor(self.ui.label_pin_inclined,'green')
    #     # self.setBarColor(self.ui.label_overall,'green')
    #     # if glue_det:
    #     #     self.setBarColor(self.ui.label_glue,'red')
    #     #     pass#sql写数据库
    #     # if pin_glue_det:
    #     #     self.setBarColor(self.ui.label_pin_glue,'red')
    #     # if pin_inclined_det:
    #     #     self.setBarColor(self.ui.label_pin_inclined,'red')
    #     # if glue_det or pin_glue_det or pin_inclined_det:
    #     #     self.setBarColor(self.ui.label_overall,'red')
        
    def remove(self):# 申请剔除次品
        plcM2=self.plc_listen.readM(2)
        self.plc_docheck.setBit(plcM2,2,False)
        self.plc_docheck.writeM(2,plcM2)
        pass
    def setBarColor(self,bar,color):#这只检测界面状态颜色
        tmpimg=None
        if 'green'==color:
            tmpimg=QImage(self.imggreenbar.data,self.imggreenbar.shape[1], self.imggreenbar.shape[0],QImage.Format_RGB888) 
        elif 'red'==color:
            tmpimg=QImage(self.imgredbar.data,self.imggreenbar.shape[1], self.imggreenbar.shape[0],QImage.Format_RGB888)
        pixmapImg = QPixmap.fromImage(tmpimg).scaled(80,40)
        bar.setPixmap(pixmapImg)
        pass

    def openCamera(self,i=0):
        camManager = self.camManager
        # 打开相机
        camManager.getDeviceInfo(camManager.deviceList.pDeviceInfo[i])
        camera = camManager.openDevice(i)
        # 与拍摄方向绑定
        camManager.setOrientation('left', camera)
        return camera



    def getParams(self,orientation:str='left')->dict: # 获取设备参数

        params = {}
        # params['height']=self.camManager.getCameraParams(orientation,'Height')
        # params['width'] = self.camManager.getCameraParams(orientation, 'Width')
        # params['acquisitionFrameRate'] = self.camManager.getCameraParams(orientation,"AcquisitionFrameRate")
        # params['exposureTime'] = self.camManager.getCameraParams(orientation,"ExposureTime")
        params['Height'] = self.camera.getParam('Height')
        params['Width'] = self.camera.getParam('Width')
        params['AcquisitionFrameRate'] = self.camera.getParam('AcquisitionFrameRate')
        params['ExposureTime'] = self.camera.getParam('ExposureTime')
        return params

    def getConveyorSpeed(self):
        params = {}
        params['conveyorSpeed'] = self.conveyor.getSpeed()
        return params

    def setCameraParams(self,params,orientation:str='left'):
        self.camManager.setCameraParams(orientation,'Height',int(params['height']))
        self.camManager.setCameraParams(orientation,'Width',int(params['width']))
        self.camManager.setCameraParams(orientation,"AcquisitionFrameRate", float(params['acquisitionRate']))
        self.camManager.setCameraParams(orientation,'ExposureTime',float(params['exTime']))

    def setConveyorSpeed(self,params):
        self.conveyor.setSpeed((params['conveyorSpeed']))


    def __del__(self):
        #self.plc.destroy()
        pass

if __name__ == '__main__':
    app = QApplication([])
    mainW = MainWindowLogic()

    app.exec()