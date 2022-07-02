# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setCameraParams.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_SetCameraParams(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.setCameraHeight = QLineEdit(self.centralwidget)
        self.setCameraHeight.setObjectName(u"setCameraHeight")
        self.setCameraHeight.setGeometry(QRect(130, 60, 141, 41))
        font = QFont()
        font.setPointSize(12)
        self.setCameraHeight.setFont(font)
        self.setCameraWidth = QLineEdit(self.centralwidget)
        self.setCameraWidth.setObjectName(u"setCameraWidth")
        self.setCameraWidth.setGeometry(QRect(130, 120, 141, 41))
        self.setCameraWidth.setFont(font)
        self.label_Height = QLabel(self.centralwidget)
        self.label_Height.setObjectName(u"label_Height")
        self.label_Height.setGeometry(QRect(40, 60, 81, 31))
        font1 = QFont()
        font1.setPointSize(13)
        self.label_Height.setFont(font1)
        self.label_Width = QLabel(self.centralwidget)
        self.label_Width.setObjectName(u"label_Width")
        self.label_Width.setGeometry(QRect(40, 120, 71, 31))
        self.label_Width.setFont(font1)
        self.label_Exposuretime = QLabel(self.centralwidget)
        self.label_Exposuretime.setObjectName(u"label_Exposuretime")
        self.label_Exposuretime.setGeometry(QRect(30, 190, 111, 31))
        self.label_Exposuretime.setFont(font)
        self.setExposuretime = QLineEdit(self.centralwidget)
        self.setExposuretime.setObjectName(u"setExposuretime")
        self.setExposuretime.setGeometry(QRect(140, 190, 131, 41))
        self.setExposuretime.setFont(font)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(50, 273, 101, 41))
        self.pushButton.setFont(font1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.pushButton.clicked.connect(MainWindow.setCameraParams)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_Height.setText(QCoreApplication.translate("MainWindow", u"\u76f8\u673a\u9ad8\u5ea6\uff1a", None))
        self.label_Width.setText(QCoreApplication.translate("MainWindow", u"\u76f8\u673a\u5bbd\u5ea6\uff1a", None))
        self.label_Exposuretime.setText(QCoreApplication.translate("MainWindow", u"Exposuretime:", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u63d0\u4ea4", None))
    # retranslateUi

