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
#from get_faces_from_camera import *
import dlib
import numpy as np  # 数据处理的库numpy
import cv2          # 图像处理的库OpenCv
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# dlib预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# cap.set(propId, value)
# 设置视频参数，propId设置的视频参数，value设置的参数值
#self.cap.set(3, 480)

# 截图screenshoot的计数器
cnt_ss = 0

# 人脸截图的计数器
cnt_p = 0

# 保存
path_save = "D:/FACE/Face_Recognition_PYQT5/data/get_from_camera/"


class Face_Register(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.label = QLabel(self)
        self.label.setFixedWidth(300)
        self.label.setFixedHeight(300)
        self.label.move(20, 20)
        self.pixMap = QPixmap("Face_Recognition.jpg").scaled(self.label.width(), self.label.height())
        self.label.setPixmap(self.pixMap)
        self.label.show()

        self.startButton = QPushButton('start', self)
        self.startButton.move(400, 200)
        self.capPictureButton = QPushButton('capPicture', self)
        self.capPictureButton.move(400, 250)

        self.startButton.clicked.connect(self.start)
        self.capPictureButton.clicked.connect(self.cap)

        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)

        self.userName = QLineEdit(self)
        self.userName.setPlaceholderText('User Name')
        self.userName.setFixedSize(200, 30)
        self.userName.move(350, 50)
        self.passWordLine = QLineEdit(self)
        self.passWordLine.setEchoMode(QLineEdit.Password)
        self.passWordLine.setPlaceholderText('Pass Word')
        self.passWordLine.setFixedSize(200, 30)
        self.passWordLine.move(350, 120)

    def start(self, event):
        self.cap = cv2.VideoCapture(0)
        #self.cv2.imshow()

        self.timer.timeout.connect(self.capPicture)
    def cap(self,event):
        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
        self.cap.release()
        feature = cal_feature(self.face)
        print('PPPPPPPPPPPPPPPPPPPPPPP')
        #np.save('usrfeature.npy', ALLFEATURE)
        sim = cal_cos(feature,np.array(ALLFEATURE))
        m = np.argmax(sim) #返回array中数值最大数的下标，默认将输入array视作一维，出现相同的最大，返回第一次出现的
        if max(sim)>0.9:
            print(sim, USRNAME)
            QMessageBox.information(self,"Information","Welcome," + USRNAME[m])
        else:
            QMessageBox.information(self,"Information","识别失败!")
        self.label.setPixmap(self.pixMap)

    def capPicture(self):

        if (self.cap.isOpened()):
            # get a frame
            flag, im_rd = self.cap.read()#用来判断图像是否读取成功/读到了视频末尾
            kk = cv2.waitKey(1)     #延时毫秒
            print(kk)
            img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)#取灰度

            rects = detector(img_gray, 0)#人脸数

            print(rects)
            # 待会要写的字体
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(im_rd, "no face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            ##########
            #"""
            if len(rects) != 0:# 检测到人脸
                print("hehhehehe")
                for k, d in enumerate(rects):
                    # 计算矩形大小,(x,y), (宽度width, 高度height)
                    #pos_start = tuple([d.left(), d.top()])
                    #pos_end = tuple([d.right(), d.bottom()])
                    # 计算矩形框大小
                    #height = d.bottom() - d.top()
                    #width = d.right() - d.left()

                    height, width, bytesPerComponent = im_rd.shape
                    bytesPerLine = bytesPerComponent * width
                    print("+++++++++++++++++")
                    print(height,width)
                    print(bytesPerComponent)
                    print(bytesPerLine)
                    print("+++++++++++++++++")
                    # 变换彩色空间顺序
                    cv2.cvtColor(im_rd, cv2.COLOR_BGR2RGB, im_rd)
                    # 转为QImage对象
                    self.image = QImage(im_rd.data, width, height, bytesPerLine, QImage.Format_RGB888)
                    self.label.setPixmap(QPixmap.fromImage(self.image).scaled(self.label.width(), self.label.height()))#没有这两句调用不出摄像头


                    # 根据人脸大小生成空的图像
                    cv2.rectangle(im_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)
                    im_blank = np.zeros((height, width, 3), np.uint8)

                # 显示人脸数
                cv2.putText(im_rd, "faces: " + str(len(rects)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

            else:
                # 没有检测到人脸
                cv2.putText(im_rd, "no face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            #"""
            # 添加说明
            im_rd = cv2.putText(im_rd, "s: save face", (20, 400), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
            im_rd = cv2.putText(im_rd, "q: quit", (20, 450), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
