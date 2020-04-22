# 20180625 加入了多线程 ，效果不好
# 20180625 加入了输入框名称
import sys
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
    QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer
import dlib
import numpy as np  # 数据处理的库numpy
import cv2          # 图像处理的库OpenCv
import requests
import threading
import json
import winsound
import time

# url 设置
#url_recognize_local = "http://localhost:8080/recognize"
#url_register_local = "http://localhost:8080/register"
#url_recognize_local = "http://cms.zhbitcs.com/recognize"
#url_register_local = "http://cms.zhbitcs.com/register"
url_recognize_local = "http://cms.zhbitcs.com:801/recognize"
url_register_local = "http://cms.zhbitcs.com:801/register"

# dlib预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 截图screenshoot的计数器
cnt_ss = 0

# 人脸截图的计数器
cnt_p = 0
# 源摄像文件保存路径
source_path_save = "D:/pic/"
source_file_name = "source.jpg"

class Face_Register(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.label = QLabel(self)
        self.label.setFixedWidth(500)
        self.label.setFixedHeight(400)
        self.label.move(20, 20)
        self.pixMap = QPixmap("timg.jpg").scaled(self.label.width(), self.label.height())
        self.label.setPixmap(self.pixMap)
        self.label.show()

        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)

        self.USER_ID_Name = QLabel (self)
        self.USER_ID_Name.setText(u"用户名:")
        self.USER_ID_Name.move(520, 50)

        self.USER_ID = QLineEdit(self)
        self.USER_ID.setPlaceholderText('USER ID')
        self.USER_ID.setText("1001")
        self.USER_ID.setFixedSize(150, 30)
        self.USER_ID.move(600, 50)

        self.Building_ID_Name = QLabel(self)
        self.Building_ID_Name.setText(u"楼栋号:")
        self.Building_ID_Name.move(520,120)

        self.Building_ID = QLineEdit(self)
        self.Building_ID.setPlaceholderText('Building ID')
        self.Building_ID.setText ("202")
        self.Building_ID.setFixedSize(150, 30)
        self.Building_ID.move(600, 120)

        self.Community_ID_Name = QLabel (self)
        self.Community_ID_Name.setText (u"社区号:")
        self.Community_ID_Name.move (520, 190)

        self.Community_ID = QLineEdit(self)
        self.Community_ID.setPlaceholderText('Community ID')
        self.Community_ID.setText ("66")
        self.Community_ID.setFixedSize(150, 30)
        self.Community_ID.move(600, 190)

        self.Card_ID_Name = QLabel (self)
        self.Card_ID_Name.setText (u"卡  号:")
        self.Card_ID_Name.move (520, 260)

        self.Card_ID = QLineEdit(self)
        self.Card_ID.setPlaceholderText('Card ID')
        self.Card_ID.setText("201806")
        self.Card_ID.setFixedSize(150, 30)
        self.Card_ID.move(600, 260)

        self.startButton = QPushButton('start', self)
        self.startButton.move(600, 320)

        self.startButton.clicked.connect(self.start)


    def start(self, event):
        self.cap = cv2.VideoCapture(0)#打开摄像头
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.thread)
        self.timer.start(2000)  # 设置时间隔并启动

    def Show_Camera(self):#用来判断图像是否读取成功/读到了视频末尾
        while self.cap.isOpened():
        #if (self.cap.isOpened()):
            flag, im_rd = self.cap.read()
            '''#注释掉截图
            img_gray = cv2.cvtColor(im_rd, cv2.COLOR_BGR2GRAY)#取灰度
            rects = detector(img_gray, 0)
            if len(rects) != 0:
                # 检测到人脸
                # 矩形框
                for k, d in enumerate(rects):
                    # 计算矩形大小
                    # (x,y), (宽度width, 高度height)
                    pos_start = tuple([d.left(), d.top()])
                    pos_end = tuple([d.right(), d.bottom()])

                    # 计算矩形框大小
                    height = d.bottom() - d.top()
                    width = d.right() - d.left()

                    # 根据人脸大小生成空的图像
                    cv2.rectangle(im_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)
                    im_blank = np.zeros((height, width, 3), np.uint8)

                    cnt_p =0
                    for ii in range(height):
                        for jj in range(width):
                            im_blank[ii][jj] = im_rd[d.top() + ii][d.left() + jj]
                    # 存储人脸图像文件
                    cv2.imwrite(source_path_save + "img_face_" + str(cnt_p) + ".jpg", im_blank)
                    print("写入本地：", source_path_save + "img_face_" + str(cnt_p) + ".jpg")
            '''
            # 变换彩色空间顺序
            cv2.cvtColor(im_rd, cv2.COLOR_BGR2RGB, im_rd)
            h, w, bytesPerComponent = im_rd.shape
            bytesPerLine = bytesPerComponent * w
            self.image = QImage(im_rd.data, w, h, bytesPerLine, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.image).scaled(self.label.width(), self.label.height()))#QImage转化为QPixmap，scaled根据label的长度和高度比例进行缩小
            time.sleep(0.5)
        #self.cap.release()

    def recognize(self):
        if (self.cap.isOpened()):
            ret, img = self.cap.read()
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)# 取灰度
            rects = detector(img_gray, 0)# 人脸数rects
            font = cv2.FONT_HERSHEY_SIMPLEX# 待会要写的字体
            if len(rects) != 0:
                print('抓到你！')
                '''
                # 矩形框
                for k, d in enumerate(rects):
                    # 绘制矩形框
                    im_rd = cv2.rectangle(im_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]),
                                          (0, 255, 255), 2)
                '''

                # 检测到人脸
                cv2.imwrite(source_path_save+source_file_name, img)
                file = open(source_path_save+source_file_name, 'rb')
                USER_ID = self.USER_ID.text()
                Building_ID = self.Building_ID.text()
                Commuity_ID = self.Community_ID.text()
                Card_ID = self.Card_ID.text()

                self.kv2 = {"communityid": Commuity_ID, "buildingid": Building_ID, "width": 320, "height": 240,"cardid": Card_ID, "regnew": 1,"format": 1}
                r = requests.post(url_recognize_local, params=self.kv2, data=file)
                #print(self.kv2)
                #print(r.url)
                print(r.status_code)
                print(r.headers)
                print(r.text)
                '''
                data = json.loads(r.text)
                # print("%s;%s" % (data['ok'], data['id']))  # 可能只有data['ok']键值
                if str(data['ok']) == 'True':
                    if data['id'] != 0:
                        # Play Windows exit sound.
                        # winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                        winsound.PlaySound('ll.wav', flags=1)
                        #  第一个参数是频率，频率越大，音调越尖；  第二个数字是声音持续时间，单位是毫秒
                        # winsound.Beep(600, 1000)
                        time.sleep(2)
                        print("delay 2 sec")
                    else:
                        winsound.PlaySound('adjust1.wav', flags=1)
                        #  第一个参数是频率，频率越大，音调越尖；  第二个数字是声音持续时间，单位是毫秒
                        # winsound.Beep(600, 1000)
                        time.sleep(2)
                        print("delay 2 sec")
                '''

            else:
                # 没有检测到人脸
                #后面可以增加语音提示，同时用一个定时器定时调用响应
                print('没人啦！还看！')
                #cv2.putText(img, "no face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    def thread(self):
        threads = []
        t1 = threading.Thread(target=self.Show_Camera)
        threads.append(t1)
        t2 = threading.Thread(target=self.recognize)
        threads.append(t2)

        t2.setDaemon(True)#把t2设置为守护进程，那么主线程结束时候，t2无论执行完没有都会被结束
        t2.start()
        t1.start()
        #t1.join()
        '''
        for t in threads:
            #t.setDaemon(True)#设置守护进程
            t.start()
        '''
        #for t in threads:
        #t.join()