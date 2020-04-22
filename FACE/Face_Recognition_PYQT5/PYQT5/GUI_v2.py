from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QDialog,
    QApplication, QPushButton, QDesktopWidget, QLineEdit, QTabWidget)
#from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QImage, QPalette, QBrush
import sys
import cv2
import numpy


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


model_def = 'VGG_FACE_deploy.prototxt'
model_weights = 'VGG_Face_finetune_1000_iter_900.caffemodel'
# create transformer for the input called 'data'


class faceSign(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setFixedWidth(260)
        self.label.setFixedHeight(200)
        self.label.move(20, 15)
        self.pixMap = QPixmap("timg1.jpg").scaled(self.label.width(),self.label.height())
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

class Dialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.resize(240, 200)
        #self.resize(240, 200)
        self.label = QLabel(self)
        self.label.setFixedWidth(150)
        self.label.setFixedHeight(150)
        self.label.move(40, 20)

        pixMap = QPixmap("timg.jpg").scaled(self.label.width(),self.label.height())
        self.label.setPixmap(pixMap)
        self.label.show()
        self.timer = QTimer()
        self.timer.start()
        self.timer.setInterval(100)
        self.cap = cv2.VideoCapture(0)
        self.timer.timeout.connect(self.capPicture)

    def mousePressEvent(self, event):
        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
        self.cap.release()##释放摄像头
        NEWFEATURE = cal_feature(self.face).reshape([1,-1])
        if NEWFEATURE.size > 0:
            for key, value in tempUsrName.items():
                ALLUSER[key] = value
                USRNAME.append(key)
                with open('ALLUSER.pickle', 'wb') as f:
                    pickle.dump(ALLUSER, f)
                with open('USRNAME.pickle', 'wb') as f:
                    pickle.dump(USRNAME, f)
                print(ALLFEATURE,NEWFEATURE)
                ALLFEATURE = np.concatenate((ALLFEATURE, NEWFEATURE), axis=0)
                np.save('usrfeature.npy', ALLFEATURE)
                QMessageBox.information(self,"Information","Success!")


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

class passWordSign(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        #self.setGeometry(0, 0, 450, 300)
        self.signUpButton = QPushButton(QIcon('timg.jpg'), 'Sign up', self)
        self.signUpButton.move(300, 200)#设置按键的位置
        self.signInButton = QPushButton(QIcon('camera.png'), 'Sign in', self)
        self.signInButton.move(200, 200)

        self.usrNameLine = QLineEdit( self )
        self.usrNameLine.setPlaceholderText('User Name')#设置框里面的灰度字
        self.usrNameLine.setFixedSize(200, 30)#设置框的大小
        self.usrNameLine.move(100, 50)#设置框的位置
        self.passWordLine = QLineEdit(self)
        self.passWordLine.setEchoMode(QLineEdit.Password)
        self.passWordLine.setPlaceholderText('Pass Word')
        self.passWordLine.setFixedSize(200, 30)
        self.passWordLine.move(100, 120)

        self.signInButton.clicked.connect(self.signIn)#添加“登陆”槽
        self.signUpButton.clicked.connect(self.signUp)#添加“注册”槽
        self.show()

    def signIn(self):
        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME    #定义全局变量

        if self.usrNameLine.text() not in ALLUSER:
            QMessageBox.information(self,"Information","用户不存在，请注册")#发送一个弹窗或者一个回复信息给它
        elif ALLUSER[self.usrNameLine.text()] == self.passWordLine.text():
            QMessageBox.information(self,"Information","Welcome!")

        else:
            QMessageBox.information(self,"Information","密码错误!")

    def signUp(self):
        global ALLFEATURE, NEWFEATURE, tempUsrName, ALLUSER, USRNAME
        if self.usrNameLine.text() in ALLUSER:
            QMessageBox.information(self,"Information","用户已存在!")

        elif len(self.passWordLine.text()) < 3: #可以手动设置密码的最小长度，后面有时间可以增加密码的安全性提示，比如字母，首密码应该是什么格式的之类
            QMessageBox.information(self,"Information","密码太短!")
        else:
            tempUsrName.clear()
            tempUsrName[self.usrNameLine.text()] = self.passWordLine.text()
            self.addPicture()


    def addPicture(self):
        dialog = Dialog(parent=self)
        dialog.show()

class TabWidget(QTabWidget):

    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)

        self.setWindowTitle('ZHBIT智能门禁')
        self.setWindowIcon(QIcon('timg1.jpg'))#窗口的左上角图标
        self.resize(600, 480)
        self.center()#调用下面的居中函数

        self.mContent = passWordSign()#调用
        self.mIndex = faceSign()#调用

        self.addTab(self.mContent, QIcon('login.jpg'), u"密码登录")
        self.addTab(self.mIndex, QIcon('login.jpg'),u"人脸识别")

        palette=QPalette()#调色板
        icon=QPixmap('login.jpg').scaled(600, 260)#背景图片
        palette.setBrush(self.backgroundRole(), QBrush(icon)) #添加背景图片
        self.setPalette(palette)

    def center(self):#让界面居中

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):#退出确认框

        reply = QMessageBox.question(self, 'Message',
            "你确定?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    t = TabWidget()
    t.show()
    #ex = Example()
    sys.exit(app.exec_())