import sys
from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
                             QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer

#import caffe
import numpy as np
import os
import sys
import cv2
import dlib

# new add below
import cv2
import dlib         # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2          # 图像处理的库OpenCv
import requests     # request post
import time

# url 设置
url_recognize_local = "http://localhost:8080/recognize"
url_register_local = "http://localhost:8080/register"

kv = {"communityid": 97, "buildingid": 643, "width": 320, "height": 240, "format": 1}
kv2 = {"communityid": 97, "buildingid": 643, "width": 320, "height": 240, "cardid": 5348765, "regnew": 1, "format": 1}

# 源摄像文件保存路径
source_path_save = "D:/pic/"
source_file_name = "source.jpg"


# dlib预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
# new add above

'''
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

model_def = 'VGG_FACE_deploy.prototxt'
model_weights = 'VGG_Face_finetune_1000_iter_900.caffemodel'


# 计算余弦距离
def cal_cos(A, B):
    num = A.dot(B.T)  # 若为行向量则 A * B.T
    print(B.shape)
    if B.ndim == 1:
        denom = np.linalg.norm(A) * np.linalg.norm(B)
    else:
        denom = np.linalg.norm(A) * np.linalg.norm(B, axis=1)
    # print(num)
    cos = num / denom  # 余弦值
    sim = 0.5 + 0.5 * cos  # 归一化
    return sim


#def cal_feature(image):
    # for i,img_name in enumerate(os.listdir(path)):
    # image = caffe.io.load_image(os.path.join(path,img_name))
    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[0, :, :, :] = transformed_image
    output = net.forward()
    return net.blobs['fc7'].data[0]

'''
class passWordSign(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setFixedWidth(500)
        self.label.setFixedHeight(400)
        self.label.move(20, 15)
        self.pixMap = QPixmap("D:/pic/14.jpg").scaled(self.label.width(), self.label.height())
        self.label.setPixmap(self.pixMap)
        self.label.show()
        self.usrNameLine = QLineEdit(self)
        self.usrNameLine.setPlaceholderText('User Name')
        self.usrNameLine.setFixedSize(200, 30)
        self.usrNameLine.move(550, 70)
        self.passWordLine = QLineEdit(self)
        self.passWordLine.setEchoMode(QLineEdit.Password)
        self.passWordLine.setPlaceholderText('Pass Word')
        self.passWordLine.setFixedSize(200, 30)
        self.passWordLine.move(550, 160)
        self.startButton = QPushButton('start', self)
        self.startButton.move(600, 240)
        self.capPictureButton = QPushButton('capPicture', self)
        self.capPictureButton.move(600, 320)
        self.startButton.clicked.connect(self.start)
        self.capPictureButton.clicked.connect(self.cap)
        # self.cap = cv2.VideoCapture(0)
        # self.ret, self.img = self.cap.read()
        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)

    def start(self, event):
        self.cap = cv2.VideoCapture(0)
        self.timer.timeout.connect(self.capPicture)

    def cap(self, event):
        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
        self.cap.release()
        feature = cal_feature(self.face)
        # np.save('usrfeature.npy', ALLFEATURE)
        sim = cal_cos(feature, np.array(ALLFEATURE))
        m = np.argmax(sim)
        if max(sim) > 0.9:
            print(sim, USRNAME)
            QMessageBox.information(self, "Information", "Welcome," + USRNAME[m])
        else:
            QMessageBox.information(self, "Information", "识别失败!")
        self.label.setPixmap(self.pixMap)

    def capPicture(self):
        if (self.cap.isOpened()):
            # get a frame
            ret, img = self.cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                roi_color = img[y:y + h, x:x + w]
                self.face = cv2.resize(img[y:y + h, x:x + w], (224, 224), interpolation=cv2.INTER_CUBIC)
            height, width, bytesPerComponent = img.shape
            bytesPerLine = bytesPerComponent * width
            # 变换彩色空间顺序
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
            # 转为QImage对象
            self.image = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(self.image).scaled(self.label.width(), self.label.height()))




class faceSign(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setFixedWidth(500)
        self.label.setFixedHeight(400)
        self.label.move(20, 15)
        self.pixMap = QPixmap("d:/pic/13.jpg").scaled(self.label.width(), self.label.height())
        self.label.setPixmap(self.pixMap)
        self.label.show()
        self.startButton = QPushButton('start', self)
        self.startButton.move(600, 70)
       # self.capPictureButton = QPushButton('capPicture', self)
       # self.capPictureButton.move(600, 190)
        self.startButton.clicked.connect(self.start)
       # self.capPictureButton.clicked.connect(self.cap)
        # self.cap = cv2.VideoCapture(0)
        # self.ret, self.img = self.cap.read()
        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)

    def start(self, event):
        self.cap = cv2.VideoCapture(0)
        self.timer.timeout.connect(self.capPicture)
        self.timer.timeout.connect(self.recognize)

    def cap(self, event):
        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
        self.cap.release()
        feature = cal_feature(self.face)
        # np.save('usrfeature.npy', ALLFEATURE)
        sim = cal_cos(feature, np.array(ALLFEATURE))
        m = np.argmax(sim)
        if max(sim) > 0.9:
            print(sim, USRNAME)
            QMessageBox.information(self, "Information", "Welcome," + USRNAME[m])
        else:
            QMessageBox.information(self, "Information", "识别失败!")
        self.label.setPixmap(self.pixMap)

    def capPicture(self):
        if (self.cap.isOpened()):
            ret, img = self.cap.read()
            #self.capPicture().img = img
            height, width, bytesPerComponent = img.shape
            bytesPerLine = bytesPerComponent * width
            # 变换彩色空间顺序
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
            # 转为QImage对象
            self.image = QImage(img.data,width, height, bytesPerLine, QImage.Format_RGB888)
            self.pixMap = QPixmap(self.image).scaled(self.label.width(), self.label.height())
            self.label.setPixmap(self.pixMap)


    def recognize(self):
        # 取灰度
        ret, img = self.cap.read()
        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # 人脸数rects
        rects = detector(img_gray, 0)

        # print(len(rects))

        # 待会要写的字体
        font = cv2.FONT_HERSHEY_SIMPLEX
        if len(rects) != 0:
            # 检测到人脸
            cv2.imwrite(source_path_save + source_file_name, img)
            file = open(source_path_save + source_file_name, 'rb')
            r = requests.post(url_recognize_local, params=kv, data=file)
            print(r.status_code)
            print(r.headers)
            print(r.text)
            # 显示人脸数
            cv2.putText(img, "faces: " + str(len(rects)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            # 没有检测到人脸
            cv2.putText(img, "no face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)


class TabWidget(QTabWidget):

    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.setWindowTitle('Face Recognition')
        self.setWindowIcon(QIcon('camera.png'))
        self.resize(800, 460)
        self.center()
        self.mContent = passWordSign()
        self.mIndex = faceSign()
        self.addTab(self.mContent, QIcon('camera.png'), u"人脸注册")
        self.addTab(self.mIndex, u"人脸识别")
        palette = QPalette()
        icon = QPixmap('background.jpg').scaled(400, 260)
        palette.setBrush(self.backgroundRole(), QBrush(icon))  # 添加背景图片
        self.setPalette(palette)

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = TabWidget()
    t.show()
    # ex = Example()
    sys.exit(app.exec_())