# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'IPView.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)

class Ui_IPAddress(object):
    def setupUi(self, IPAddress):
        if not IPAddress.objectName():
            IPAddress.setObjectName(u"IPAddress")
        IPAddress.resize(800, 602)
        self.label = QLabel(IPAddress)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(360, 40, 91, 41))
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label_3 = QLabel(IPAddress)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(440, 130, 91, 41))
        font1 = QFont()
        font1.setPointSize(14)
        self.label_3.setFont(font1)
        self.label_4 = QLabel(IPAddress)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(90, 190, 91, 41))
        self.label_4.setFont(font1)
        self.lineEdit_PLCIP = QLineEdit(IPAddress)
        self.lineEdit_PLCIP.setObjectName(u"lineEdit_PLCIP")
        self.lineEdit_PLCIP.setGeometry(QRect(530, 130, 151, 41))
        self.lineEdit_PLCIP.setFont(font1)
        self.label_6 = QLabel(IPAddress)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(90, 250, 91, 41))
        self.label_6.setFont(font1)
        self.label_8 = QLabel(IPAddress)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(90, 310, 91, 41))
        self.label_8.setFont(font1)
        self.lineEdit_camera3IP = QLineEdit(IPAddress)
        self.lineEdit_camera3IP.setObjectName(u"lineEdit_camera3IP")
        self.lineEdit_camera3IP.setGeometry(QRect(190, 250, 151, 41))
        self.lineEdit_camera3IP.setFont(font1)
        self.label_9 = QLabel(IPAddress)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(440, 310, 91, 41))
        self.label_9.setFont(font1)
        self.lineEdit_localIP = QLineEdit(IPAddress)
        self.lineEdit_localIP.setObjectName(u"lineEdit_localIP")
        self.lineEdit_localIP.setGeometry(QRect(190, 130, 151, 41))
        self.lineEdit_localIP.setFont(font1)
        self.lineEdit_camera1IP = QLineEdit(IPAddress)
        self.lineEdit_camera1IP.setObjectName(u"lineEdit_camera1IP")
        self.lineEdit_camera1IP.setGeometry(QRect(190, 190, 151, 41))
        self.lineEdit_camera1IP.setFont(font1)
        self.label_2 = QLabel(IPAddress)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 130, 91, 41))
        self.label_2.setFont(font1)
        self.label_5 = QLabel(IPAddress)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(440, 190, 91, 41))
        self.label_5.setFont(font1)
        self.lineEdit_AcquisitionFrameRate_5 = QLineEdit(IPAddress)
        self.lineEdit_AcquisitionFrameRate_5.setObjectName(u"lineEdit_AcquisitionFrameRate_5")
        self.lineEdit_AcquisitionFrameRate_5.setGeometry(QRect(530, 310, 151, 41))
        self.lineEdit_AcquisitionFrameRate_5.setFont(font1)
        self.lineEdit_camera4IP = QLineEdit(IPAddress)
        self.lineEdit_camera4IP.setObjectName(u"lineEdit_camera4IP")
        self.lineEdit_camera4IP.setGeometry(QRect(530, 250, 151, 41))
        self.lineEdit_camera4IP.setFont(font1)
        self.lineEdit_camera2IP = QLineEdit(IPAddress)
        self.lineEdit_camera2IP.setObjectName(u"lineEdit_camera2IP")
        self.lineEdit_camera2IP.setGeometry(QRect(530, 190, 151, 41))
        self.lineEdit_camera2IP.setFont(font1)
        self.lineEdit_camera5IP = QLineEdit(IPAddress)
        self.lineEdit_camera5IP.setObjectName(u"lineEdit_camera5IP")
        self.lineEdit_camera5IP.setGeometry(QRect(190, 310, 151, 41))
        self.lineEdit_camera5IP.setFont(font1)
        self.label_7 = QLabel(IPAddress)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(440, 250, 91, 41))
        self.label_7.setFont(font1)
        self.pushButton_back = QPushButton(IPAddress)
        self.pushButton_back.setObjectName(u"pushButton_back")
        self.pushButton_back.setGeometry(QRect(400, 440, 121, 51))
        self.pushButton_back.setFont(font)
        self.pushButton_editIP = QPushButton(IPAddress)
        self.pushButton_editIP.setObjectName(u"pushButton_editIP")
        self.pushButton_editIP.setGeometry(QRect(250, 440, 121, 51))
        self.pushButton_editIP.setFont(font)

        self.retranslateUi(IPAddress)

        QMetaObject.connectSlotsByName(IPAddress)
    # setupUi

    def retranslateUi(self, IPAddress):
        IPAddress.setWindowTitle(QCoreApplication.translate("IPAddress", u"Form", None))
        self.label.setText(QCoreApplication.translate("IPAddress", u"IP\u5730\u5740", None))
        self.label_3.setText(QCoreApplication.translate("IPAddress", u"PLC IP\uff1a", None))
        self.label_4.setText(QCoreApplication.translate("IPAddress", u"\u76f8\u673a1 IP\uff1a", None))
        self.lineEdit_PLCIP.setText("")
        self.label_6.setText(QCoreApplication.translate("IPAddress", u"\u76f8\u673a3 IP\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("IPAddress", u"\u76f8\u673a5 IP\uff1a", None))
        self.label_9.setText(QCoreApplication.translate("IPAddress", u"*****", None))
        self.label_2.setText(QCoreApplication.translate("IPAddress", u"\u672c\u673aIP\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("IPAddress", u"\u76f8\u673a2 IP\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("IPAddress", u"\u76f8\u673a4 IP\uff1a", None))
        self.pushButton_back.setText(QCoreApplication.translate("IPAddress", u"\u8fd4\u56de", None))
        self.pushButton_editIP.setText(QCoreApplication.translate("IPAddress", u"\u786e\u5b9a", None))
    # retranslateUi

