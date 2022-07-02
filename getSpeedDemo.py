from PySide6.QtWidgets import QMainWindow, QApplication

from device import Conveyor
from getSpeed import Ui_GetSpeed
from communicate.plcCommunicate import S7_200Smart_PLC,PESensorCom,ConveyorCom
from snap7 import client


class MainWindow(QMainWindow):
    def __init__(self):  # 初始化
        super().__init__()
        self.ui = Ui_GetSpeed()
        self.ui.setupUi(self)
        self.plc_watchdog = S7_200Smart_PLC()
        # 传送带对象
        self.conveyor = Conveyor(self.plc_watchdog)

    #获取传送带速度
    def getSpeed(self):
        # 创建与PLC的链接
        self.plc_watchdog.connect_200smart("192.168.3.50")
        speed = self.conveyor.getSpeed()
        print(speed)
        self.ui.textBrowser.setText("speed:" + str(speed))


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()

    app.exec()