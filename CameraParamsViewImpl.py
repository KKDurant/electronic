from PySide6.QtWidgets import QMainWindow, QApplication

from CameraParamsView import Ui_CameraParams
from camera import CamManager, Camera


class Camera_Params_View(QMainWindow):
    def __init__(self,Initial_View,camera):
        super(Camera_Params_View, self).__init__()
        self.camera = camera
        # 保存好父窗口，用于返回后显示父窗口
        self.parent = Initial_View

        self.cameraParams = Ui_CameraParams()
        self.cameraParams.setupUi(self)

        self.cameraParams.pushButton_editParams.clicked.connect(self.editCameraParams)
        self.cameraParams.pushButton_back.clicked.connect(self.back)

        height = self.camera.getParam("Height") # 2的倍数
        width = self.camera.getParam("Width") # 4的倍数
        acquisitionFrameRate = self.camera.getParam("AcquisitionFrameRate")
        exposureTime = self.camera.getParam("ExposureTime")

        self.cameraParams.lineEdit_CameraHeight.setText(str(height))
        self.cameraParams.lineEdit_CameraWidth.setText(str(width))
        self.cameraParams.lineEdit_AcquisitionFrameRate.setText(str(acquisitionFrameRate))
        self.cameraParams.lineEdit_ExpasureTime.setText(str(exposureTime))
        # self.camera.closeDevice()

    def back(self):
        self.close()
        self.parent.show()

    def editCameraParams(self):

        # 获取文本框里的内容
        height = self.cameraParams.lineEdit_CameraHeight.text()
        width = self.cameraParams.lineEdit_CameraWidth.text()
        acquisitionFrameRate = self.cameraParams.lineEdit_AcquisitionFrameRate.text()
        exposureTime = self.cameraParams.lineEdit_ExpasureTime.text()

        print('exposureTime',exposureTime)

        self.camera.setParam("Height", int(height))
        self.camera.setParam("Width", int(width))
        self.camera.setParam("AcquisitionFrameRate", float(acquisitionFrameRate))
        self.camera.setParam("ExposureTime", float(exposureTime))



        print('height:',self.camera.getParam("Height"))

        self.close()
        self.parent.show()
        self.camera.closeDevice()

if __name__ == '__main__':
    app = QApplication()
    camera_params_window = Camera_Params_View()
    camera_params_window.show()

    app.exec()