from time import sleep
from PySide6.QtWidgets import QApplication,QMainWindow,QComboBox
from PySide6.QtUiTools import QUiLoader
from threading import Thread
from mainWindowLogicOri import MainWindowLogic

app = QApplication([])
mainui = QUiLoader().load('ui/camera_params.ui')
mainui.show()
mymain = MainWindowLogic(mainui)
mymain.startup()
t1 = Thread(target=mymain.listen, args=())
t1.start()
app.exec()
