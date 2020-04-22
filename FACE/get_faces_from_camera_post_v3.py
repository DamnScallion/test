# created at 2018-05-11
# updated at 2018-05-29
# By law
# 添加了新增的功能 r:recognize ,n:register

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
predictor = dlib.shape_predictor('D:/FACE/Face_Recognition_PYQT5/shape_predictor_68_face_landmarks.dat')

# 创建cv2摄像头对象
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('rtsp://admin:zhbit000123@10.11.178.91:554/h264/ch1/main/av_stream') # 海康视频流

# cap.set(propId, value)
# 设置视频参数，propId设置的视频参数，value设置的参数值
cap.set(3, 480)
cap.set(4, 640)


# cap.isOpened（） 返回true/false 检查初始化是否成功
while cap.isOpened():

    # cap.read()
    # 返回两个值：
    #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
    #    图像对象，图像的三维矩阵q
    flag, im_rd = cap.read()
    # time.sleep(1)

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
        if kk == ord('r'):
            cv2.imwrite(source_path_save + source_file_name, im_rd)
            file = open(source_path_save+source_file_name,'rb')
            r = requests.post(url_recognize_local, params=kv , data=file)
            print(r.status_code)
            print(r.headers)
            print(r.text)
        if kk == ord('n'):
            cv2.imwrite(source_path_save + source_file_name, im_rd)
            file = open(source_path_save + source_file_name, 'rb')
            r = requests.post(url_register_local, params=kv2, data=file)
            print (r.status_code)
            print (r.headers)
            print (r.text)

        # 显示人脸数
        cv2.putText(im_rd, "faces: " + str(len(rects)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    else:
        # 没有检测到人脸
        cv2.putText(im_rd, "no face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # 添加说明
    im_rd = cv2.putText(im_rd, "q: quit ; r: recognize ; n: register", (20, 430), font, 0.8, (55, 55, 255), 1,
                        cv2.LINE_AA)
    # 按下q键退出
    if kk == ord('q'):
        break
    # 窗口显示
    cv2.namedWindow("camera", 0)  # 如果需要摄像头窗口大小可调
    cv2.imshow("camera", im_rd)


# 释放摄像头
cap.release()
print("cap_release")

# 删除建立的窗口
cv2.destroyAllWindows()
