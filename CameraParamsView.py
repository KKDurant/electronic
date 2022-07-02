# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CameraParamsView.ui'
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

class Ui_CameraParams(object):
    def setupUi(self, CameraParams):
        if not CameraParams.objectName():
            CameraParams.setObjectName(u"CameraParams")
        CameraParams.resize(800, 600)
        self.centralwidget = QWidget(CameraParams)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(340, 20, 111, 41))
        font = QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 90, 91, 41))
        font1 = QFont()
        font1.setPointSize(14)
        self.label_2.setFont(font1)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(440, 90, 91, 41))
        self.label_3.setFont(font1)
        self.lineEdit_CameraHeight = QLineEdit(self.centralwidget)
        self.lineEdit_CameraHeight.setObjectName(u"lineEdit_CameraHeight")
        self.lineEdit_CameraHeight.setGeometry(QRect(190, 90, 151, 41))
        self.lineEdit_CameraHeight.setFont(font1)
        self.lineEdit_CameraWidth = QLineEdit(self.centralwidget)
        self.lineEdit_CameraWidth.setObjectName(u"lineEdit_CameraWidth")
        self.lineEdit_CameraWidth.setGeometry(QRect(530, 90, 151, 41))
        self.lineEdit_CameraWidth.setFont(font1)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(90, 150, 91, 41))
        self.label_4.setFont(font1)
        self.lineEdit_AcquisitionFrameRate = QLineEdit(self.centralwidget)
        self.lineEdit_AcquisitionFrameRate.setObjectName(u"lineEdit_AcquisitionFrameRate")
        self.lineEdit_AcquisitionFrameRate.setGeometry(QRect(190, 150, 151, 41))
        self.lineEdit_AcquisitionFrameRate.setFont(font1)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(440, 150, 91, 41))
        self.label_5.setFont(font1)
        self.lineEdit_ExpasureTime = QLineEdit(self.centralwidget)
        self.lineEdit_ExpasureTime.setObjectName(u"lineEdit_ExpasureTime")
        self.lineEdit_ExpasureTime.setGeometry(QRect(530, 150, 151, 41))
        self.lineEdit_ExpasureTime.setFont(font1)
        self.lineEdit_AcquisitionFrameRate_2 = QLineEdit(self.centralwidget)
        self.lineEdit_AcquisitionFrameRate_2.setObjectName(u"lineEdit_AcquisitionFrameRate_2")
        self.lineEdit_AcquisitionFrameRate_2.setGeometry(QRect(190, 210, 151, 41))
        self.lineEdit_AcquisitionFrameRate_2.setFont(font1)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(90, 210, 91, 41))
        self.label_6.setFont(font1)
        self.lineEdit_AcquisitionFrameRate_3 = QLineEdit(self.centralwidget)
        self.lineEdit_AcquisitionFrameRate_3.setObjectName(u"lineEdit_AcquisitionFrameRate_3")
        self.lineEdit_AcquisitionFrameRate_3.setGeometry(QRect(530, 210, 151, 41))
        self.lineEdit_AcquisitionFrameRate_3.setFont(font1)
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(460, 210, 91, 41))
        self.label_7.setFont(font1)
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(90, 270, 91, 41))
        self.label_8.setFont(font1)
        self.lineEdit_AcquisitionFrameRate_4 = QLineEdit(self.centralwidget)
        self.lineEdit_AcquisitionFrameRate_4.setObjectName(u"lineEdit_AcquisitionFrameRate_4")
        self.lineEdit_AcquisitionFrameRate_4.setGeometry(QRect(190, 270, 151, 41))
        self.lineEdit_AcquisitionFrameRate_4.setFont(font1)
        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(470, 270, 91, 41))
        self.label_9.setFont(font1)
        self.lineEdit_AcquisitionFrameRate_5 = QLineEdit(self.centralwidget)
        self.lineEdit_AcquisitionFrameRate_5.setObjectName(u"lineEdit_AcquisitionFrameRate_5")
        self.lineEdit_AcquisitionFrameRate_5.setGeometry(QRect(530, 270, 151, 41))
        self.lineEdit_AcquisitionFrameRate_5.setFont(font1)
        self.pushButton_editParams = QPushButton(self.centralwidget)
        self.pushButton_editParams.setObjectName(u"pushButton_editParams")
        self.pushButton_editParams.setGeometry(QRect(250, 380, 121, 51))
        self.pushButton_editParams.setFont(font)
        self.pushButton_back = QPushButton(self.centralwidget)
        self.pushButton_back.setObjectName(u"pushButton_back")
        self.pushButton_back.setGeometry(QRect(400, 380, 121, 51))
        self.pushButton_back.setFont(font)
        CameraParams.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(CameraParams)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        CameraParams.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(CameraParams)
        self.statusbar.setObjectName(u"statusbar")
        CameraParams.setStatusBar(self.statusbar)

        self.retranslateUi(CameraParams)

        # self.pushButton.clicked.connect(MainWindow.setCameraParams)
        # self.pushButton_editParams.clicked.connect(self.editCameraParams)
        # self.pushButton_editParams.clicked.connect(CameraParams.editCameraParams)

        QMetaObject.connectSlotsByName(CameraParams)
    # setupUi

    def retranslateUi(self, CameraParams):
        CameraParams.setWindowTitle(QCoreApplication.translate("CameraParams", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("CameraParams", u"\u76f8\u673a\u53c2\u6570", None))
        self.label_2.setText(QCoreApplication.translate("CameraParams", u"\u76f8\u673a\u9ad8\u5ea6\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("CameraParams", u"\u76f8\u673a\u5bbd\u5ea6\uff1a", None))
        self.lineEdit_CameraWidth.setText("")
        self.label_4.setText(QCoreApplication.translate("CameraParams", u"\u5206\u8fa8\u7387\uff1a", None))
        self.label_5.setText(QCoreApplication.translate("CameraParams", u"\u66dd\u5149\u65f6\u95f4\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("CameraParams", u"*****:", None))
        self.label_7.setText(QCoreApplication.translate("CameraParams", u"******\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("CameraParams", u"*****:", None))
        self.label_9.setText(QCoreApplication.translate("CameraParams", u"*****:", None))
        self.pushButton_editParams.setText(QCoreApplication.translate("CameraParams", u"\u786e\u5b9a", None))
        self.pushButton_back.setText(QCoreApplication.translate("CameraParams", u"\u8fd4\u56de", None))
    # retranslateUi

