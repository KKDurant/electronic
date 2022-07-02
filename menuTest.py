from time import sleep
from PySide6.QtWidgets import QApplication,QMainWindow,QComboBox
from PySide6.QtUiTools import QUiLoader
from threading import Thread
from mainWindowLogic import MainWindowLogic

app = QApplication([])
mainui = QUiLoader().load('ui/detection.ui')


mymain = MainWindowLogic(mainui)
def showStatics():
    print("sta")
    pass
#menubar= mainui.menuBar()
#statics = menubar.addMenu("统计信息")
#showhistory = statics.addAction("showHistory")
#showhistory.triggered.connect(showStatics)
#mymain.doCheck()

showhistory = mainui.menuBar().menu.addAction("showHistory")
showhistory.triggered.connect(showStatics)
mainui.show()
app.exec()