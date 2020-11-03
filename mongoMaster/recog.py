import numpy as np
from cv2 import cv2
import os
import face_recognition

# 人脸识别分类器
faceCascade = cv2.CascadeClassifier(
    r'/Users/haodongsheng/.local/share/virtualenvs/hellopy-X998b6LV/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml')

save_dir = r'/Users/haodongsheng/Documents/Prog/mongoMaster/face/'

def get_video_path(dir_path,target_path):
    list_ = os.listdir(dir_path)
    for i in range(0, len(list_)):
        path = os.path.join(dir_path, list_[i])
        if os.path.isdir(path):
            get_video_path(path,target_path)
        if os.path.isfile(path):
             temp_path = str.lower(path)
             if temp_path.endswith(".mp4"):
                recognize(path,target_path)

def recognize(file_path,target_path,tolerance=0.5):
    global faceCascade
    global save_dir
    # 开启摄像头
    cap = cv2.VideoCapture(file_path)

    target_image = face_recognition.load_image_file(target_path)
    target_image_encodings = face_recognition.face_encodings(target_image)
    if  not target_image_encodings or len(target_image_encodings) == 0:
        print('目标图片错误,没有人脸')
        exit(0)
    currentFrame = 0
    frame = cap.get(7)
    frame = int(frame)
    ok = True
    while currentFrame < frame:
        print('正在识别...当前文件路径为'+file_path+'当帧为'+str(currentFrame))
        # 读取摄像头中的图像，ok为是否读取成功的判断参数
        ok, img = cap.read()
        if ok == False:
            print('fail')
            break
        currentFrame = currentFrame + 100
        # 转换成灰度图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 人脸检测
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(32, 32)
        )
        if not isinstance(faces, tuple):
            rgb_small_frame = img[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if face_locations:
                print('识别成功,当前文件路径为'+file_path+'当帧为'+str(currentFrame))
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)
                if face_encodings:
                    results = face_recognition.compare_faces(
                        face_encodings, target_image_encodings[0], tolerance=tolerance)
                    print('匹配成功人脸，当前文件路径为'+file_path+'当帧为'+str(currentFrame))
                    print(results)
                    if results and len(results)>0:
                        for success in results:
                            if success == True:
                               print('请注意，当前文件路径为'+file_path+'当帧为'+str(currentFrame))
                               file_path_list = file_path.split('/')
                               file_name = file_path_list[-1]
                               file_name = file_name[0:-4]
                               cv2.imwrite(save_dir+'.'+file_name+'-'+str(currentFrame)+'.png',img) 
                               exit(0)
                            else:
                               cv2.imwrite(save_dir+'.'+ str(currentFrame)+'.png',img) 
        # 画矩形
        # currentFaceInOnePic = 0
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # cropImage = img[y: (y+h), x: (x+w)]
        # cv2.imwrite(r'/Users/haodongsheng/Documents/Prog/hellopy/face/'+ str(currentFrame)+'-'+str(currentFaceInOnePic)+'.png',cropImage)
        # currentFaceInOnePic = currentFaceInOnePic + 1

        # cv2.imshow('video', img)

        # k = cv2.waitKey(1)
        # if k == 27:    # press 'ESC' to quit
        #     break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # recognize('/Volumes/MongoDBStudy/.supergate$/.a/.a/bin/20200516/最强露脸巨乳女骑师多次高潮Ch.mp4',r'/Users/haodongsheng/Documents/Prog/mongoMaster/face/.7000.png')
    get_video_path(r'/Volumes/MongoDBStudy/.supergate$/.a/.a/bin/20200516',r'/Users/haodongsheng/Documents/Prog/mongoMaster/face/.7000.png')