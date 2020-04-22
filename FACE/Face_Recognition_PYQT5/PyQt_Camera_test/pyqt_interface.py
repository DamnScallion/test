import cv2
import sys
import os
import pickle
global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
import numpy as np
import caffe

from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
    QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer

class faceSign(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setFixedWidth(260)
        self.label.setFixedHeight(200)
        self.label.move(20, 15)
        self.pixMap = QPixmap("face.jpg").scaled(self.label.width(),self.label.height())
        self.label.setPixmap(self.pixMap)
        self.label.show()
        self.startButton = QPushButton('start', self)
        self.startButton.move(300, 50)
        self.capPictureButton = QPushButton('capPicture', self)
        self.capPictureButton.move(300, 150)
        self.startButton.clicked.connect(self.start)
        self.capPictureButton.clicked.connect(self.cap)
        #self.cap = cv2.VideoCapture(0)
        #self.ret, self.img = self.cap.read()
        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)



    def start(self,event):
        self.cap = cv2.VideoCapture(0)
        self.timer.timeout.connect(self.capPicture)

    def cap(self,event):
        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
        self.cap.release()
        feature = cal_feature(self.face)
        #np.save('usrfeature.npy', ALLFEATURE)
        sim = cal_cos(feature,np.array(ALLFEATURE))
        m = np.argmax(sim)
        if max(sim)>0.9:
            print(sim, USRNAME)
            QMessageBox.information(self,"Information","Welcome," + USRNAME[m])
        else:
            QMessageBox.information(self,"Information","识别失败!")
        self.label.setPixmap(self.pixMap)

    def capPicture(self):

        if (self.cap.isOpened()):
            # get a frame
            ret, img = self.cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
                self.face = cv2.resize(img[y:y+h, x:x+w],(224, 224), interpolation=cv2.INTER_CUBIC)
            height, width, bytesPerComponent = img.shape
            bytesPerLine = bytesPerComponent * width
            # 变换彩色空间顺序
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
            # 转为QImage对象
            self.image = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.image).scaled(self.label.width(),self.label.height()))