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
                isConnect = {}
                # 获取相机是否已连接
                if result:
                    # cameraLeftIsConnect = 'True'
                    isConnect['cameraLeftIsConnect'] = 'True'
                # 获取PLC是否已连接 如果能获取到传送带速度，那就是已连接的
                if result2:
                    isConnect['PLCIsConnect'] = 'True'

                result.update(result2)
                result.update(isConnect)

                re['type'] = 'getDeviceParamsReply'
                re['content'] = result
                re["statusCode"] = 200
                print(re)

            # 修改设备参数
            elif re['type'] == 'alterParams':
                # 获取Java端传过来的设备参数值
                params = re['content']
                print("java端传过来的设备参数值：",params)
                # self._mainW.setCameraParams(params,'left')
                if params['cameraOrientation'] == '左':
                    params['cameraOrientation'] = 'left'
                print(params['cameraOrientation'])
                self._mainW.setCameraParams(params,params['cameraOrientation'])
                self._mainW.setConveyorSpeed(params)
                nparray = self._mainW.camManager.getOneFrame(params['cameraOrientation'])
                imgBGR = cv2.cvtColor(nparray, cv2.COLOR_RGB2BGR)
                # cvRGBImg = cv2.cvtColor(imgBGR, cv2.COLOR_RGB2BGR)
                encode_image = cv2.imencode(".jpg", imgBGR)[1]
                byte_data = encode_image.tobytes()
                base64_str = base64.b64encode(byte_data).decode("ascii")
                params = self._mainW.getParams(params['cameraOrientation'])
                speedParam = self._mainW.getConveyorSpeed()
                params.update(speedParam)
                re['type'] = 'setDeviceParamsReply'
                params['ImageResult'] = base64_str
                re['content'] = params
                re['statusCode'] = 200

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