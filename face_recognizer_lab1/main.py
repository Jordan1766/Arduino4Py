import shutil
import os
import cv2
import face_recognizer_lab1.Face_capture_positives as cap
import face_recognizer_lab1.Face_recognition as recogn
import face_recognizer_lab1.Face_training as train
from face_recognizer_lab1 import Config

def menu():
    while True:
        print('--------------')
        print('1. 拍照片-製作素材')
        print('   訓練-機器學習')
        print('2. 辨識-人臉辨識')
        print('9. 離開-Exit')
        print('--------------')
        n = int(input('請選擇: '))

        if n == 1:
            shutil.rmtree(Config.TRAINING_FOLDER)
            my_name = input('請輸入英文名')
            Config.MY_NAME = my_name
            cap.capture()
            cv2.waitKey(1)
            train.train()
        elif n == 2:
            score = recogn.recognizer()
            print("score:", score)
            cv2.waitKey(1)
        elif n == 9:
            print('Exit')
            break



if '__main__' == __name__:
    menu()

