# created at 2018-05-11
# updated at 2018-05-29
# By law
# 添加了新增的功能 r:recognize ,n:register

import dlib         # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2          # 图像处理的库OpenCv
import requests     # request post
import time
import threading
import json
import winsound

# url 设置
#url_recognize_local = "http://localhost:8080/recognize"
#url_register_local = "http://localhost:8080/register"
url_recognize_local = "http://cms.zhbitcs.com:801/recognize"
url_register_local = "http://cms.zhbitcs.com:801/register"

kv = {"communityid": 97, "buildingid": 643, "width": 320, "height": 240, "format": 1}
kv2 = {"communityid": 97, "buildingid": 643, "width": 320, "height": 240, "cardid": 5348766, "regnew": 1, "format": 1}

# 源摄像文件保存路径
source_path_save = "D:/FACE/Face_Recognition_PYQT5/pic"
source_file_name = "source.jpg"


# dlib预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('D:/FACE/Face_Recognition_PYQT5/shape_predictor_68_face_landmarks.dat')

# 识别成功标识位
ok_flag = 0

# 创建cv2摄像头对象
cap = cv2.VideoCapture(0)

# cap.set(propId, value)
# 设置视频参数，propId设置的视频参数，value设置的参数值
cap.set(3, 480)
cap.set(4, 640)

def camera_show():
    # cap.isOpened（） 返回true/false 检查初始化是否成功
    while cap.isOpened():

        # cap.read()
        # 返回两个值：
        #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
        #    图像对象，图像的三维矩阵q
        flag, im_rd = cap.read()

        cv2.waitKey (1)
        # 待会要写的字体
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(im_rd, "ZHBIT Face recognition", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        # 窗口显示
        cv2.namedWindow("camera", 0)  # 如果需要摄像头窗口大小可调
        cv2.imshow("camera", im_rd)

    # 释放摄像头
    cap.release()

    # 删除建立的窗口
    cv2.destroyAllWindows()

def recognize():
    # cap.isOpened（） 返回true/false 检查初始化是否成功
    while cap.isOpened():

        # cap.read()
        # 返回两个值：
        #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
        #    图像对象，图像的三维矩阵q
        flag, im_rd = cap.read()
        #time.sleep(1)

        # 每帧数据延时1ms，延时为0读取的是静态帧
        kk = cv2.waitKey(1)

        # 取灰度
        img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

        # 人脸数rects
        rects = detector(img_gray, 0)

        #print(len(rects))

        # 待会要写的字体
        font = cv2.FONT_HERSHEY_SIMPLEX

        if len(rects) != 0:
            # 检测到人脸
            cv2.imwrite(source_path_save + source_file_name, im_rd)
            file = open(source_path_save+source_file_name,'rb')
            r = requests.post(url_recognize_local, params=kv , data=file)
            print(r.status_code)
            print(r.headers)
            print(r.text)
            data = json.loads(r.text)
            #print("%s;%s" % (data['ok'], data['id']))  # 可能只有data['ok']键值
            if str(data['ok']) == 'True':
                if data['id'] != 0:
                    # Play Windows exit sound.
                    #winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    winsound.PlaySound('sign.wav', flags=1)
                    #  第一个参数是频率，频率越大，音调越尖；  第二个数字是声音持续时间，单位是毫秒
                    #winsound.Beep(600, 1000)
                    time.sleep(2)
                    print("delay 2 sec")

threads = []
t1 = threading.Thread(target=camera_show)
threads.append(t1)
t2 = threading.Thread(target=recognize)
threads.append(t2)


if __name__ == '__main__':
    #camera_show()

    for t in threads:
        t.setDaemon (True)
        t.start ()
    t.join ()
