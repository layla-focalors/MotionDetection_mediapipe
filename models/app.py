import cv2
import mediapipe as mp
import numpy as np
import argparse
import random
import time
from pythonosc import udp_client
import pymysql
import uuid
import datetime
import json
from collections import OrderedDict
file_data = OrderedDict()
import pandas as pd
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="OSC ServerIP")
parser.add_argument("--port", type=int, default=9001, help="Lisener") 
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
df = pd.DataFrame()
IMAGE_FILES = []
BG_COLOR = (192, 192, 192)  # 회색
cap = cv2.VideoCapture(0)

i = 0

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("카메라를 찾을 수 없습니다.")
            continue
        value = []
        
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        # print('Nose world landmark:'),
        try:
            x = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
            y = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
            z = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE].z
            visi = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE].visibility

            file_data["data"] = {'x':x, 'y':y, 'z':z, 'vision':visi}
            print(json.dumps(file_data, ensure_ascii=False, indent="\t"))
            jsonp = json.dumps(file_data, ensure_ascii=False, indent="\t")
            
            client.send_message("/key", i)
            client.send_message("/x_origin", x)
            client.send_message("/y_origin", y)
            client.send_message("/z_origin", z)
            client.send_message("/visi", visi)
            client.send_message("/json", jsonp)
            
            # time.sleep(1)
            i += 1
            if i == 33:
                print("I 재설정! 성공")
                i = 0
            
        except:
            print("스캔중인 사물 없음! : 대기모드")
        
            
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()