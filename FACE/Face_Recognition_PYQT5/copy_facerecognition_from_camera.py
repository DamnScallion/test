import dlib         # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2          # 图像处理的库OpenCv
import csv          #创建csv文件
import time
import math
from numba import jit
from get_features_into_CSV import arrayooo
# face recognition model, the object maps human faces into 128D vectors
#人脸识别模型，对象将人脸映射到128D矢量
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")#残差网络

# 计算两个向量间的欧式距离，此函数时间耗费基本可以忽略不计
@jit
def return_euclidean_distance(feature_1, feature_2):
    feature_1 = np.array(feature_1)#将输入数据转化为一个ndarray数组,features_1对应的是传进来的视频中的实时数据
    feature_2 = np.array(feature_2)#将输入数据转化为一个ndarray数组，features_2对应的是传进来的前面已经计算好的特征均值，两个feature计算时间加起来，时间耗费大概在0.0003s

    dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))#欧式距离的思想:大约是0.00002s的时间
    print(dist)
    if dist > 0.4:
        return "strangers"
    else:
        return "friends"

#用get_feature_into_CSV中的compute_the_mean(path_csv_rd)计算出的均值赋给features_mean_default_person
features_mean_default_person = arrayooo

# dlib预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')#shape_predictor_68_face_landmarks.dat是已经训练好的人脸关键点检测器

# 创建cv2摄像头对象
cap = cv2.VideoCapture(0)

# cap.set(propId, value)
# 设置视频参数，propId设置的视频参数，value设置的参数值
cap.set(3, 480)

# 计算并且返回单张图像的128D特征
def get_128d_features(img_gray):#img_gray为传进来的参数，img_gray实际为系统当前截取一帧的图像
    dets = detector(img_gray, 1)#dets为识别出的人脸位置，例如，测试可知，dets=rectangles[[(191, 217) (414, 440)]]（不唯一，仅供参考），时间耗费大概在0.2s
    if len(dets) != 0:
        shape = predictor(img_gray, dets[0])#时间耗费大概在0.002s，即2ms左右
        face_descriptor = facerec.compute_face_descriptor(img_gray, shape)#时间耗费最大，0.5s以上
    else:
        face_descriptor = 0
    return face_descriptor

# cap.isOpened（） 返回true/false 检查初始化是否成功
while cap.isOpened():

    # cap.read()
    # 返回两个值：
    #    一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
    #    图像对象，图像的三维矩阵
        # flag的值为True或者False，代表有没有读到图片，im_rd代表当前截取的一帧的图片
    flag, im_rd = cap.read()
        # 每帧数据延时1ms，延时为0读取的是静态帧
    kk = cv2.waitKey(1)
        # 将当前截取的彩色图像转化为灰度
    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

    # 人脸数dets
    dets = detector(img_gray, 0)

    # 待会要写的字体
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(im_rd, "q: quit", (20, 400), font, 0.8, (84, 255, 159), 1, cv2.LINE_AA)

    if len(dets) != 0:

        features_rd = get_128d_features(im_rd)#时间耗费大概在0.18s到0.19s

        start = time.clock()
        compare = return_euclidean_distance(features_rd, features_mean_default_person)#时间耗费0.5s
        elapsed = (time.clock() - start)
        print("Compare Time:")
        print("Time used:", elapsed)
        print("faces: " + str(len(dets)))
    else:
        print("No faces!")
    # 按下q键退出
    if kk == ord('q'):
        break

    # 窗口显示
    cv2.imshow("camera", im_rd)

# 释放摄像头
cap.release()
# 删除建立的窗口
cv2.destroyAllWindows()
