# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
    QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer
import numpy as np
import os
import pickle

from Face_Recognition import Recognition
from Face_Register_v2 import Face_Register
#from Setting import Setting
#from ID_manage import ID_manage



face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class Ui_MainWindow(QTabWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.setWindowTitle('ZHBIT Face recognition access control')
        self.setWindowIcon(QIcon('timg.jpg'))
        self.resize(800, 480)
        self.center()

#        self.Recognition = Recognition()#调用函数Camera()进行人脸识别，界面设计在函数中
        self.Recognition = Recognition()  # 调用函数Camera()进行人脸识别，界面设计在函数中
        self.Register = Face_Register()#调用函数Face_Register()进行人脸识别，界面设计在函数中
#        self.ID_manage = ID_manage()#调用函数ID_manage()进行人脸识别，界面设计在函数中
        #self.Setting = Setting()#调用函数Setting()进行人脸识别，界面设计在函数中

        self.addTab(self.Recognition, QIcon('Face_Recognition.jpg'),u"人脸识别")
        self.addTab(self.Register, QIcon('login.jpg'), u"人脸注册")
        #self.addTab(self.ID_manage, QIcon('ID_manage.jpg'), u"用户管理")
        #self.addTab(self.Setting,QIcon('setting.jpg'),u"设置")
        palette=QPalette()
        icon=QPixmap('login.jpg').scaled(400, 260)
        palette.setBrush(self.backgroundRole(), QBrush(icon)) #添加背景图片
        self.setPalette(palette)
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())