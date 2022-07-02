import os
import random
import sys
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

from CameraParamsViewImpl import Camera_Params_View
from InitialView import Ui_InitialViewWindow
from camera import CamManager, Camera
from camera_params import Ui_MainWindow
from detectionModel import YoloModel
from communicate.plcCommunicate import S7_200Smart_PLC,PESensorCom,ConveyorCom
from device import *
from queue import Queue
from PIL import Image, ImageTk
from PySide6.QtGui import QImage,QPixmap
from PySide6.QtWidgets import QApplication,QMainWindow,QComboBox,QMessageBox
from PySide6.QtUiTools import QUiLoader
from device.photoelectricSensor import PhotoelectricSensor
from setCameraParams import Ui_SetCameraParams


class Initial_View(QMainWindow):
    def __init__(self):  # 初始化
        super(Initial_View,self).__init__()
        self.initial_ui = Ui_InitialViewWindow()
        self.initial_ui.setupUi(self)

        self.initial_ui.pushButton_VCamera1.clicked.connect(self.openCameraParamsView)
        self.show()

    def openCameraParamsView(self):
        self.cameraManager = CamManager()

        # self.cameraManager.openDevice(0)
        self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
        self.camera = self.cameraManager.openDevice(0)
        self.Camera_Params_window = Camera_Params_View(self,self.camera)
        self.hide()
        self.Camera_Params_window.show()

        # self.camera_paramsViewImpl.show()

    # 获取相机参数 i表示第几台相机，数值从0开始
    def getCameraParams(self):
        self.cameraManager = CamManager()

        # self.cameraManager.openDevice(0)
        self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
        camera = self.cameraManager.openDevice(0)
        height = camera.getParam("Height")
        width = camera.getParam("Width")
        QMessageBox.information(self, "参数信息", str(height) + '/' + str(width))


    # 设置相机参数
    # def setCameraParams(self):
    #     self.cameraManager = CamManager()
    #
    #     # self.cameraManager.openDevice(0)
    #     self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
    #     camera = self.cameraManager.openDevice(0)
    #     # height = camera.getParam("Height")
    #     # width = camera.getParam("Width")
    #
    #     # 获取文本框里的文本
    #     height = self.ui.setCameraHeight.text()
    #     width = self.ui.setCameraWidth.text()
    #     height = int(height)
    #     width = int(width)
    #     # 更改相机参数
    #     camera.setParam("Height",height)
    #     camera.setParam("Width",width)
    #     print(camera.getParam("Height"))
    #     print(camera.getParam("Width"))


        # print(height)
        # print(width)
        # self.ui.textBrowser.setText("height:" + str(height) + "\n" + "width:" + str(width))

if __name__ == '__main__':
    app = QApplication()
    window = Initial_View()
    # window.show()

    app.exec()