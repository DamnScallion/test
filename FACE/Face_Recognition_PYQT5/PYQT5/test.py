#! /usr/bin/python3
# coding = utf-8
# from PyQt5 import QtGui,QtCore,Qt
import sys
import cv2
from gevent.libev.corecext import SIGNAL, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainter, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget

# 线程类：
class Timer(QtCore.QThread):

    def __init__(self, signal="updateTime()", parent=None):
        super(Timer, self).__init__(parent)
        self.stoped= False
        self.signal= signal
        self.mutex= QtCore.QMutex()

    def run(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stoped= False
        while True:
            if self.stoped:
                return
            self.emit(QtCore.SIGNAL(self.signal))
            #40毫秒发送一次信号
            time.sleep(0.04)

    def stop(self):
        with QtCore.QMutexLocker(self.mutex):
            self.stoped= True

    def isStoped(self):
        with QtCore.QMutexLocker(self.mutex):
            return self.stoped

class mycsms(QMainWindow,QWidget):
    def __init__(self):
        super(mycsms, self).__init__()
        QWidget.__init__(self)
        self.setupUi(self)
        self.image = QImage()
        self.device = cv2.VideoCapture(0)
        self.playTimer = Timer("updatePlay()")
        #button = QtWidgets.QPushButton('show', self)
        self.connect(self.playTimer, SIGNAL("updatePlay()"), self.showCamer)

        #button.clicked.connect(self.playTimer)
        #button.clicked.connect(self.playTimer, SIGNAL("updatePlay()"), self.showCamer)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
    # 读摄像头
    def showCamer(self):
        if self.device.isOpened():
            ret, frame= self.device.read()
        else:
            ret = False
        # 读写磁盘方式
        # cv2.imwrite("2.png",frame)
        #self.image.load("2.png")

        height, width, bytesPerComponent= frame.shape
        bytesPerLine = bytesPerComponent* width
        # 变换彩色空间顺序
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB,frame)
        # 转为QImage对象
        self.image= QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.view.setPixmap(QPixmap.fromImage(self.image))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myshow = mycsms()
    myshow.playTimer.start()
    myshow.show()
    sys.exit(app.exec_())

