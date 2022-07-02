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
from camera import CamManager, Camera
from camera_params import Ui_MainWindow
from detectionModel import YoloModel
from communicate.plcCommunicate import S7_200Smart_PLC,PESensorCom,ConveyorCom
from device import *
from queue import Queue
from PIL import Image, ImageTk
from PySide6.QtGui import QImage,QPixmap
from PySide6.QtWidgets import QApplication,QMainWindow,QComboBox
from PySide6.QtUiTools import QUiLoader
from device.photoelectricSensor import PhotoelectricSensor

class MainWindow(QMainWindow):
    def __init__(self):  # 初始化
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # mainui = QUiLoader().load('ui/camera_params.ui')
        # 加载相机管理

        # mainui.pushButton.clicked.connect(lambda x : self.getCameraParams())

    # 获取相机参数
    def getCameraParams(self):
        self.cameraManager = CamManager()

        # self.cameraManager.openDevice(0)
        self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
        camera = self.cameraManager.openDevice(0)
        height = camera.getParam("Height")
        width = camera.getParam("Width")

        print(height)
        print(width)
        self.ui.textBrowser.setText("height:" + str(height) + "\n" + "width:" + str(width))


    # 文本显示框
    # def showCameraParams(self):




if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()

    # mainui = QUiLoader().load('ui/camera_params.ui')
    # mainwindow = Params_demo(mainui)
    # mainwindow.show()
    app.exec()
    # sys.exit(app.exec())