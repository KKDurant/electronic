import base64
import json
import os
import sys
import threading
from pathlib import Path
import socket

import cv2

from camera import CamManager
# from detectionModel import YoloModel

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # 根目录
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # 把根目录加到PATH中
CONFIGPATH = Path(os.path.join("detectionModel"))


class SendImageThread(threading.Thread):

    def connect(self, yoloModel):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("192.168.3.100", 2580))

        imageReturn = self.imageDetect(yoloModel)
        sendmsg = json.dumps(imageReturn)
        # 发送字符串数据给Java端
        client_socket.send(("%s" % sendmsg + "\r\n").encode("utf-8"))
        sys.stdout.flush()
        # client_socket.close()


    def imageDetect(self, yoloModel):
        # yoloModel = YoloModel(CONFIGPATH / "bestm_tr.pt", CONFIGPATH / "LEDDetection_m_tr.yaml")
        camManager = CamManager()
        # 打开相机
        camManager.getDeviceInfo(camManager.deviceList.pDeviceInfo[0])
        camera = camManager.openDevice(0)
        # 与拍摄方向绑定
        camManager.setOrientation('left', camera)
        # 从指定方向拍摄一帧
        nparray = camManager.getOneFrame('left')
        # 关闭相机
        camera.closeDevice()
        # 图像格式转换，从RGB转为BGR
        imgBGR = cv2.cvtColor(nparray, cv2.COLOR_RGB2BGR)
        hight = imgBGR.shape[0]
        width = imgBGR.shape[1]
        # 将图像裁剪为左右两部分
        left = imgBGR[0:hight, 0:int(0.5 * width)]
        right = imgBGR[0:hight, int(0.5 * width):width]
        # 两部分分别都进行判断，图像结果存在im_中，json结果存在dict中
        iml, content_dictl = yoloModel.run(left)
        imr, content_dictr = yoloModel.run(right)
        # 将结果图像拼接
        im0 = cv2.hconcat([iml, imr])
        # 图像格式转换，用于显示
        cvRGBImg = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR)
        encode_image = cv2.imencode(".jpg", cvRGBImg)[1]
        byte_data = encode_image.tobytes()
        base64_str = base64.b64encode(byte_data).decode("ascii")
        re = {"imageReturn": base64_str}
        # re = {"imageReturn": str(byte_data)}
        return re