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

# print(uuid)
# db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='live_scan', charset='utf8')
# cursor = db.cursor() 
# dts = uuid.split("-")
# sql = f"""CREATE TABLE {str(dts[0])} ( 
#         TIMESTAMP VARCHAR(80), 
#         LAYER_X VARCHAR(80), 
#         LAYER_Y VARCHAR(80), 
#         LAYER_Z VARCHAR(80), 
#         LAYER_VISIBILITY VARCHAR(80));"""
# # cursor.execute(sql) 
# # cursor.close
# print("db installed")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='live_scan', charset='utf8')
# cursor = db.cursor() 

# time = datetime.datetime.now()

# key = uuid.uuid4()
# splited_key = key.split("-")
# print(splited_key)


# print("hello?")
# import pymysql
# print("data receive")
# import uuid as uid
# print(uuid)
# db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='live_scan', charset='utf8')
# cursor = db.cursor() 
# dts = uuid.split("-")
# sql = f"""CREATE TABLE {str(dts[0])} ( 
#         TIMESTAMP VARCHAR(80), 
#         LAYER_X VARCHAR(80), 
#         LAYER_Y VARCHAR(80), 
#         LAYER_Z VARCHAR(80), 
#         LAYER_VISIBILITY VARCHAR(80));"""
# # cursor.execute(sql) 
# # cursor.close
# print("db installed")


# print("db create success")
df = pd.DataFrame()
IMAGE_FILES = []
BG_COLOR = (192, 192, 192)  # 회색
cap = cv2.VideoCapture(0)

i = 0

# sql = f"""CREATE TABLE {str(key)}( TIMESTAMP VARCHAR(80), LAYER_X VARCHAR(80), LAYER_Y VARCHAR(80), LAYER_Z VARCHAR(80), LAYER_VISIVILITY VARCHAR(80));"""
# cursor.execute(sql) 

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    # sql = f"""CREATE TABLE {str(key)}( TIMESTAMP VARCHAR(80), LAYER_X VARCHAR(80), LAYER_Y VARCHAR(80), LAYER_Z VARCHAR(80), LAYER_VISIVILITY VARCHAR(80));"""
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("카메라를 찾을 수 없습니다.")
            # 동영상을 불러올 경우는 'continue' 대신 'break'를 사용합니다.
            continue
        value = []
        
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        ac = []
        while True:
            for i in range(33):
            # print('Nose world landmark:'),
                try:
    
                    # x, y, z, visi
                    # db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='live_scan', charset='utf8')
                    # cursor = db.cursor() 
                    x = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
                    y = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
                    z = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE].z
                    visi = results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE].visibility
                    
                    ac.appned({"frame":i, "x":x, "y":y, "z":z, "visi":visi})
                    # ac.append(visi)
                    # sql = f"""INSERT INTO {splited_key[0]} VALUES('{time}', '{x}', '{y}', '{z}', '{visi}');"""
                    # print(results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE])
                    # print(results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE])
                    # cursor.execute(sql)
                    # json_val = json.dumps(results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE])
                    # print(json_val)
                    # db.commit()
                    # cursor.close()
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
                    # url = "localhost:11246/req"
                    # try:
                    #     response = requests.post(url, json=jsonp)
                    # except:
                    #     print("server not response")
                except:
                    pass
                print(ac)
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