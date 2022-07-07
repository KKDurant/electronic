import base64
import json
import os
import socket
import sys
import threading
import time
from pathlib import Path
from time import sleep

import cv2

from SocketCommunication.JavaImageConnect import SendImageThread
from SocketCommunication.util.DetectProductPositionByFiberSensors import detectProductPosition
from camera import CamManager
from communicate import S7_200Smart_PLC
from detectionModel import YoloModel
from device import Conveyor, PhotoelectricSensor
from entity.CameraEntity import cameraEntity
from mainWindowLogic import MainWindowLogic

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # 根目录
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # 把根目录加到PATH中
CONFIGPATH = Path(os.path.join("detectionModel"))

class SeverThreading(threading.Thread):
    def __init__(self, clientsocket, mainW : MainWindowLogic, recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        # self.yoloModel = yoloModel
        self._mainW = mainW
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding


    def receiveMsg(self):
        # 接受数据
        msg = ''
        # 从Java端读取recvsize个字节
        rec = self._socket.recv(self._recvsize)
        # 解码成字符串
        msg += rec.decode(self._encoding)
        print("解码后数据：")
        print(msg)

        # 文本接受是否完毕，因为python socket不能自己判断接收数据是否完毕
        # 所以需要自定义协议标志数据接受完毕
        if msg.strip().endswith('over'):
            msg = msg[:-4]

        # 将字符串解析成JSON格式数据
        re = json.loads(msg)
        # re = {'type':'listenProductPosition'}
        print("解析成JSON数据：")
        print(re)
        return re

    def run(self):
        print("开启线程.....")

        try:
            re = self.receiveMsg()

            # 根据消息调用方法 还有待完善
            if re['type'] == 'startConveyor':
                listenProduct = threading.Thread(target=self._mainW.listen)
                listenProduct.start()
                self._mainW.startup()

                re['type'] = 'startConveyorReply'
                re["content"] = "ok"
                re['statusCode'] = 200

            elif re['type'] == 'cameraStart':
                # self.cameraManager = CamManager()
                # self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
                # self.camera = self.cameraManager.openDevice(0)
                # re["content"] = "ok"
                # re["statusCode"] = 200
                pass

            elif re['type'] == 'stopConveyor':
                self._mainW.stop()
                re["content"] = "ok"
                re['type'] = 'stopConveyorReply'
                re['statusCode'] = 200

            elif re['type'] == 'getDeviceParams':
                result = self._mainW.getParams('left')
                result2 = self._mainW.getConveyorSpeed()
                result.update(result2)
                re['type'] = 'getDeviceParamsReply'
                re['content'] = result
                re["statusCode"] = 200
                print(re)

                # params = {}
                # self.cameraManager = CamManager()
                # self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
                # self.camera = self.cameraManager.openDevice(0)
                # height = self.camera.getParam("Height")
                # width = self.camera.getParam("Width")
                # acquisitionFrameRate = self.camera.getParam("AcquisitionFrameRate")
                # exposureTime = self.camera.getParam("ExposureTime")
                # # 获取传送带速度
                # self.plc_conveyorSpeed.connect_200smart("192.168.3.50")
                # conveyorSpeed = self.conveyor.getSpeed()
                # self.camera.closeDevice()
                # params['Height'] = height
                # params['Width'] = width
                # params['AcquisitionFrameRate'] = acquisitionFrameRate
                # params['ExposureTime'] = exposureTime
                # params['ConveyorSpeed'] = conveyorSpeed
                # re["content"] = params
                # re["statusCode"] = 200

            # 修改设备参数
            elif re['type'] == 'alterParams':
                # 获取Java端传过来的设备参数值
                params = re['content']
                print("java端传过来的设备参数值：",params)
                self._mainW.setCameraParams(params,'left')
                self._mainW.setConveyorSpeed(params)
                re["content"] = "ok"
                re['type'] = 'setDeviceParamsReply'
                re['statusCode'] = 200
                # # 得到各项参数值
                # height = params['height']
                # # print("height值为：" + height)
                # width = params['width']
                # exTime = params['exTime']
                # acquisitionRate = params['acquisitionRate']
                # conveyorSpeed = params['conveyorSpeed']
                # self.cameraManager = CamManager()
                # self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
                # self.camera = self.cameraManager.openDevice(0)
                # self.camera.setParam("Height", int(height))
                # self.camera.setParam("Width", int(width))
                # self.camera.setParam("AcquisitionFrameRate", float(acquisitionRate))
                # self.camera.setParam("ExposureTime", float(exTime))
                # # self.plc_conveyorSpeed.connect_200smart("192.168.3.50")
                # self.conveyor.setSpeed(float(conveyorSpeed))
                # self.camera.closeDevice()

            sendmsg = json.dumps(re)
            print("修改JSON数据并发送：")
            print(sendmsg)

            # 发送字符串数据给Java端
            self._socket.send(("%s" % sendmsg + "\r\n").encode(self._encoding))
            sys.stdout.flush()
            self._socket.close()
            print('----------')
            pass

        except Exception as identifier:
            re['statusCode'] = 500
            sendmsg = json.dumps(re)
            self._socket.send(("%s" % sendmsg + "\r\n").encode(self._encoding))
            # self._socket.send("500".encode(self._encoding))

            print(identifier)
            pass
        finally:
            self._socket.close()
        # print("任务结束.....")
            pass
        pass


    def __del__(self):
        pass

def main():
    yoloModel = YoloModel(CONFIGPATH / "bestm_tr.pt", CONFIGPATH / "LEDDetection_m_tr.yaml")

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()

    port = 50001

    serversocket.bind((host, port))

    serversocket.listen(5)

    myaddr = serversocket.getsockname()

    print("服务器地址：%s"%str(myaddr))

    while True:
        clientsocket, addr = serversocket.accept()
        print("连接地址：%s" % str(addr))

        try:
            startDevice = SeverThreading(clientsocket,yoloModel)
            startDevice.start()
            pass
        except Exception as identifier:
            print(identifier)
            pass
        pass

    serversocket.close()
    pass

if __name__ == '__main__':
    main()