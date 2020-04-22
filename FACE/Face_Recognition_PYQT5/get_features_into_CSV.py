#   return_128d_features()          获取某张图像的128d特征
#   write_into_csv()                将某个文件夹中的图像读取特征兵写入csv
#   compute_the_mean()              从csv中读取128d特征，并计算特征均值

import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np
import pandas as pd

path_pics = "D:/FACE/Face_Recognition_PYQT5/data/get_from_camera/"
path_csv = "D:/FACE/Face_Recognition_PYQT5/data/csvs/"

# detector to find the faces
#找到人脸的探测器
detector = dlib.get_frontal_face_detector()

# shape predictor to find the face landmarks
#形状预测器来寻找脸部地标
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")

# face recognition model, the object maps human faces into 128D vectors
#人脸识别模型，对象将人脸映射到128D矢量
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")


# 返回单张图像的128D特征
def return_128d_features(path_img):
    img = io.imread(path_img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dets = detector(img_gray, 1)

    print("检测的人脸图像：", path_img, "\n")

    # 因为有可能截下来的人脸再去检测，检测不出来人脸了
    # 所以要确保是 检测到人脸的人脸图像 拿去算特征
    if len(dets) != 0:
        shape = predictor(img_gray, dets[0])
        face_descriptor = facerec.compute_face_descriptor(img_gray, shape)
    else:
        face_descriptor = 0
        print("no face")

    # print(face_descriptor)
    return face_descriptor


# return_128d_features(path_pics+"img_face_13.jpg")

# 将文件夹中照片特征提取出来，写入csv
# 输入input:
#   path_pics:  图像文件夹的路径
#   path_csv:   要生成的csv路径

def write_into_csv(path_pics, path_csv):
    dir_pics = os.listdir(path_pics)

    with open(path_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(dir_pics)):
            # 调用return_128d_features()得到128d特征
            print("正在读的人脸图像：", path_pics + dir_pics[i])
            features_128d = return_128d_features(path_pics + dir_pics[i])
            #print(features_128d)
            # 遇到没有检测出人脸的图片跳过
            if features_128d == 0:
                i += 1
            else:
                writer.writerow(features_128d)
                print(features_128d)
                print("ppp")

# 调用write_into_csv 函数，将文件夹中照片特征提取出来，写入csv
write_into_csv(path_pics, path_csv + "default_person.csv")


path_csv_rd = "D:/FACE/Face_Recognition_PYQT5/data/csvs/default_person.csv"


# 从csv中读取数据，计算128d特征的均值
#这个特质均值是静态的，即视频实时检测时候这部分可以是已经计算好，直接用于比较的。
def compute_the_mean(path_csv_rd):
    column_names = []

    # 128列特征
    for i in range(128):
        column_names.append("features_" + str(i + 1))

    # 利用pandas读取csv
    rd = pd.read_csv(path_csv_rd, names=column_names)

    # 存放128维特征的均值
    feature_mean = []

    for i in range(128):
        tmp_arr = rd["features_" + str(i + 1)]
        tmp_arr = np.array(tmp_arr)

        # 计算某一个特征的均值
        tmp_mean = np.mean(tmp_arr)

        feature_mean.append(tmp_mean)

    #print(feature_mean)
    return feature_mean

#计算特征均值
arrayooo = compute_the_mean(path_csv_rd)
print(arrayooo)
# 创建写入csv文件方式,将计算好的特征均值写入csv文件中
#reader = csv.reader(csvFile)  # 读操作，返回的是迭代类型
#可以改进，使得创建的csv文件有自己的名称，用于区分开来
write_mean_path = 'D:/FACE/Face_Recognition_PYQT5/data/csvs/Claculated/'+'ordinary.csv'
csvFile2 = open(write_mean_path, 'w', newline='') # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile2)
writer.writerow(arrayooo)
csvFile2.close()