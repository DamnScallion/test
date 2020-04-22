# created at 2018-05-11
# updated at 2018-05-14
# By TimeStamp
# cnblogs: http://www.cnblogs.com/AdaminXie

import dlib         # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2          # 图像处理的库OpenCv

# dlib预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# 创建cv2摄像头对象
cap = cv2.VideoCapture(0)

# cap.set(propId, value)
# 设置视频参数，propId设置的视频参数，value设置的参数值
cap.set(3, 480)

# 截图screenshoot的计数器
cnt_ss = 0

# 人脸截图的计数器
cnt_p = 0

# 保存
path_save = "D:/FACE/Face_Recognition_PYQT5/data/get_from_camera/"

# cap.isOpened（） 返回true/false 检查初始化是否成功
while cap.isOpened():
    flag, im_rd = cap.read()
    kk = cv2.waitKey(1)
    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

    rects = detector(img_gray, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    if len(rects) != 0:
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

            if kk == ord('s'):
                cnt_p += 1
                for ii in range(height):
                    for jj in range(width):
                        im_blank[ii][jj] = im_rd[d.top() + ii][d.left() + jj]
                # 存储人脸图像文件
                cv2.imwrite(path_save + "img_face_" + str(cnt_p) + ".jpg", im_blank)
                print("写入本地：", path_save + "img_face_" + str(cnt_p) + ".jpg")
        cv2.putText(im_rd, "faces: " + str(len(rects)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    else:
        cv2.putText(im_rd, "no face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    im_rd = cv2.putText(im_rd, "s: save face", (20, 400), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
    im_rd = cv2.putText(im_rd, "q: quit", (20, 450), font, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

    if kk == ord('q'):
        break

    # 窗口显示
    # cv2.namedWindow("camera", 0) # 如果需要摄像头窗口大小可调
    cv2.imshow("camera", im_rd)

# 释放摄像头
#cap.release()

# 删除建立的窗口
#cv2.destroyAllWindows()
