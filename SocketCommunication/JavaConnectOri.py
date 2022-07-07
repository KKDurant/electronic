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
from mainWindowLogicOri import MainWindowLogic

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # 根目录
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # 把根目录加到PATH中
CONFIGPATH = Path(os.path.join("detectionModel"))

class SeverThreading(threading.Thread):
    def __init__(self, clientsocket,yoloModel,recvsize=1024 * 1024, encoding="utf-8"):
        threading.Thread.__init__(self)
        self.yoloModel = yoloModel
        self._socket = clientsocket
        self._recvsize = recvsize
        self._encoding = encoding
        self.mainW = MainWindowLogic()

        self.plc_start = S7_200Smart_PLC()
        self.plc_stop = S7_200Smart_PLC()
        self.plc_params = S7_200Smart_PLC()
        self.plc_listen = S7_200Smart_PLC()
        self.conveyorStart = Conveyor(self.plc_start)
        self.conveyorStop = Conveyor(self.plc_stop)
        self.conveyorParams = Conveyor(self.plc_params)
        self.peSensor = PhotoelectricSensor(self.plc_listen)

        self.plc_conveyorSpeed = S7_200Smart_PLC()
        # 传送带对象
        self.conveyor = Conveyor(self.plc_conveyorSpeed)

        pass

    def run(self):
        print("开启线程.....")

        try:
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
            print("解析成JSON数据：")
            print(re)

            # mainW = MainWindowLogic()
            # 根据消息调用方法 还有待完善
            if re['type'] == 'startConveyor':
                # self.mainW.startup()
                self.plc_start.connect_200smart("192.168.3.50")
                self.conveyorStart.run()
                re['type'] = 'startConveyorReply'
                # re["content"] = "ok"
                re['statusCode'] = 200

            elif re['type'] == 'cameraStart':
                self.cameraManager = CamManager()
                self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
                self.camera = self.cameraManager.openDevice(0)
                re["content"] = "ok"
                re["statusCode"] = 200

            elif re['type'] == 'stopConveyor':
                self.plc_stop.connect_200smart("192.168.3.50")
                self.conveyorStop.stop()
                # re["content"] = "ok"
                re['type'] = 'stopConveyorReply'
                re['statusCode'] = 200

            elif re['type'] == 'getDeviceParams':
                params = {}
                self.cameraManager = CamManager()
                self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
                self.camera = self.cameraManager.openDevice(0)
                height = self.camera.getParam("Height")
                width = self.camera.getParam("Width")
                acquisitionFrameRate = self.camera.getParam("AcquisitionFrameRate")
                exposureTime = self.camera.getParam("ExposureTime")
                # 获取传送带速度
                self.plc_conveyorSpeed.connect_200smart("192.168.3.50")
                conveyorSpeed = self.conveyor.getSpeed()


                self.camera.closeDevice()
                params['Height'] = height
                params['Width'] = width
                params['AcquisitionFrameRate'] = acquisitionFrameRate
                params['ExposureTime'] = exposureTime
                params['ConveyorSpeed'] = conveyorSpeed
                re["content"] = params
                re["statusCode"] = 200

            # 修改设备参数
            elif re['type'] == 'alterParams':
                # 获取Java端传过来的设备参数值
                params = re['content']
                print("java端传过来的设备参数值：",params)
                # 得到各项参数值
                height = params['height']
                # print("height值为：" + height)
                width = params['width']
                exTime = params['exTime']
                acquisitionRate = params['acquisitionRate']
                conveyorSpeed = params['conveyorSpeed']

                self.cameraManager = CamManager()
                self.cameraManager.getDeviceInfo(self.cameraManager.deviceList.pDeviceInfo[0])
                self.camera = self.cameraManager.openDevice(0)
                self.camera.setParam("Height", int(height))
                self.camera.setParam("Width", int(width))
                self.camera.setParam("AcquisitionFrameRate", float(acquisitionRate))
                self.camera.setParam("ExposureTime", float(exTime))
                # self.plc_conveyorSpeed.connect_200smart("192.168.3.50")
                self.conveyor.setSpeed(float(conveyorSpeed))
                self.camera.closeDevice()

            elif re['type'] == 'listenProductPosition':
                self.plc_listen.connect_200smart("192.168.3.50")
                while True:
                    # if self.peSensor.objInArea():
                    if self.peSensor.arrive():
                        re['type'] = 'productDetected'
                        re['content'] = 'True'
                        re["statusCode"] = 200
                        print(re)
                        sendmsg = json.dumps(re)
                        print("修改JSON数据并发送：")
                        print(sendmsg)

                        # 发送字符串数据给Java端
                        self._socket.send(("%s" % sendmsg + "\r\n").encode(self._encoding))
                        sys.stdout.flush()
                        self._socket.close()
                        print("关闭第一个socket")
                        # sleep(1)
                        print("开启SendImageThread线程")
                        sendImage = SendImageThread()
                        detect = threading.Thread(target=sendImage.connect,args=(self.yoloModel,))
                        detect.start()
                        # sleep(2)
                    else:
                        re['content'] = 'False'
                        # print(re)

            # elif re['content'] == 'catchImage':
            #     yoloModel = YoloModel(CONFIGPATH / "bestm_tr.pt", CONFIGPATH / "LEDDetection_m_tr.yaml")
            #     camManager = CamManager()
            #     # 打开相机
            #     camManager.getDeviceInfo(camManager.deviceList.pDeviceInfo[0])
            #     camera = camManager.openDevice(0)
            #     # 与拍摄方向绑定
            #     camManager.setOrientation('left', camera)
            #     # 从指定方向拍摄一帧
            #     nparray = camManager.getOneFrame('left')
            #     # 关闭相机
            #     camera.closeDevice()
            #     # 图像格式转换，从RGB转为BGR
            #     imgBGR = cv2.cvtColor(nparray, cv2.COLOR_RGB2BGR)
            #     hight = imgBGR.shape[0]
            #     width = imgBGR.shape[1]
            #     # 将图像裁剪为左右两部分
            #     left = imgBGR[0:hight, 0:int(0.5 * width)]
            #     right = imgBGR[0:hight, int(0.5 * width):width]
            #     # 两部分分别都进行判断，图像结果存在im_中，json结果存在dict中
            #     iml, content_dictl = yoloModel.run(left)
            #     imr, content_dictr = yoloModel.run(right)
            #     # 将结果图像拼接
            #     im0 = cv2.hconcat([iml, imr])
            #     # 图像格式转换，用于显示
            #     cvRGBImg = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)
            #     encode_image = cv2.imencode(".jpg", cvRGBImg)[1]
            #     byte_data = encode_image.tobytes()
            #     base64_str = base64.b64encode(byte_data).decode("ascii")
            #     re['content'] = base64_str


            # 修改JSON数据并转换成字符串
            # re["content"] = "ok"

            sendmsg = json.dumps(re)
            print("修改JSON数据并发送：")
            print(sendmsg)

            # 发送字符串数据给Java端
            self._socket.send(("%s" % sendmsg + "\r\n").encode(self._encoding))
            sys.stdout.flush()
            self._socket.close()
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

        print("任务结束.....")
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