import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

import pygame
import cv2
import mediapipe as mp
import numpy as np
from flask import Flask, render_template, Response

#Initialize the Flask app
app = Flask(__name__)


hands = mp.solutions.hands.Hands(max_num_hands=1)

pygame.init()

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))


font = pygame.font.Font('THSarabunNewBold.ttf',90)

# The main loop
cap = cv2.VideoCapture(0)


def gen_frames():
    global cnt
    global flag_box1 
    global flag_box2 
    global flag_box3 
    global flag_box4 
    flag_box1 = 0
    flag_box2 = 0
    flag_box3 = 0
    flag_box4 = 0
    cnt = 0

    cnt = 0
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            print("err")
            break
        else:
            cx8, cy8 = 0,0
            ret, img = cap.read()
            img = cv2.flip(img,1)

            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            h, w, c = img.shape

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    point8 = handLms.landmark[8]                   
                    cx8, cy8 = int(point8.x*w), int(point8.y*h)
                    cv2.circle(img,(cx8,cy8),15,(0,255,255),-1)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img,'A',(20+20,120), font, 4,(0,255,255),10,cv2.LINE_AA)
                    cv2.putText(img,'B',(175+20,120), font, 4,(0,255,255),10,cv2.LINE_AA)
                    cv2.putText(img,'C',(330+20,120), font, 4,(0,255,255),10,cv2.LINE_AA)
                    cv2.putText(img,'D',(485+20,120), font, 4,(0,255,255),10,cv2.LINE_AA)
                    cv2.rectangle(img,(20,20),(135,135),(0,255,0),10)
                    cv2.rectangle(img,(175,20),(175+135,135),(0,255,0),10)
                    cv2.rectangle(img,(330,20),(330+135,135),(0,255,0),10)
                    cv2.rectangle(img,(485,20),(485+135,135),(0,255,0),10)
                    box1 = pygame.draw.rect(display_surface,(0,255,0),(20,20,135,135),1)
                    box2 = pygame.draw.rect(display_surface,(0,255,0),(175,20,135,135),1)
                    box3 = pygame.draw.rect(display_surface,(0,255,0),(330,20,135,135),1)
                    box4 = pygame.draw.rect(display_surface,(0,255,0),(485,20,135,135),1)
                 
                    
                    if box1.collidepoint(cx8,cy8):
                        if(flag_box1 == 1):
                            cnt = cnt + 1
                        else:
                            cnt = 0
                            flag_box1 = 1
                            flag_box2 = 0
                            flag_box3 = 0
                            flag_box4 = 0

                        if cnt > 20:
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            cv2.rectangle(img,(20,20),(135,135),(0,150,180),-1)
                            cv2.putText(img,'A',(20+20,120), font, 4,(0,0,255),10,cv2.LINE_AA)
                            cv2.putText(img,'Test Mode A',(20+20,300), font, 2,(0,0,255),5,cv2.LINE_AA)
         
                    if box2.collidepoint(cx8,cy8):
                        if(flag_box2 == 1):
                            cnt = cnt + 1
                        else:
                            cnt = 0
                            flag_box1= 0
                            flag_box2 = 1
                            flag_box3 = 0
                            flag_box4 = 0

                        if cnt > 20:
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            cv2.rectangle(img,(175,20),(175+135,135),(0,150,180),-1)
                            cv2.putText(img,'B',(175+20,120), font, 4,(0,0,255),10,cv2.LINE_AA)
                            cv2.putText(img,'Test Mode B',(20+20,300), font, 2,(0,0,255),5,cv2.LINE_AA)
      
                    if box3.collidepoint(cx8,cy8):
                        if(flag_box3 == 1):
                            cnt = cnt + 1
                        else:
                            cnt = 0
                            flag_box1= 0
                            flag_box2 = 0
                            flag_box3 = 1
                            flag_box4 = 0

                        if cnt > 20:
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            cv2.rectangle(img,(330,20),(330+135,135),(0,150,180),-1)
                            cv2.putText(img,'C',(330+20,120), font, 4,(0,0,255),10,cv2.LINE_AA)
                            cv2.putText(img,'Test Mode C',(20+20,300), font, 2,(0,0,255),5,cv2.LINE_AA)
                             
                    if box4.collidepoint(cx8,cy8):
                        if(flag_box4 == 1):
                            cnt = cnt + 1
                        else:
                            flag_box1= 0
                            flag_box2 = 0
                            flag_box3 = 0
                            flag_box4 = 1

                        if cnt > 20:
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            cv2.rectangle(img,(485,20),(485+135,135),(0,150,180),-1)
                            cv2.putText(img,'D',(485+20,120), font, 4,(0,0,255),10,cv2.LINE_AA)
                            cv2.putText(img,'Test Mode D',(20+20,300), font, 2,(0,0,255),5,cv2.LINE_AA)

            else:
                cnt = 0
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img,'Press to START',(20+20,300), font, 2,(0,0,255),10,cv2.LINE_AA)
                cv2.putText(img,'A',(20+20,120), font, 4,(0,255,255),10,cv2.LINE_AA)
                cv2.putText(img,'B',(175+20,120), font, 4,(0,255,255),10,cv2.LINE_AA)
                cv2.putText(img,'C',(330+20,120), font, 4,(0,255,255),10,cv2.LINE_AA)
                cv2.putText(img,'D',(485+20,120), font, 4,(0,255,255),10,cv2.LINE_AA)
                cv2.rectangle(img,(20,20),(135,135),(0,255,0),10)
                cv2.rectangle(img,(175,20),(175+135,135),(0,255,0),10)
                cv2.rectangle(img,(330,20),(330+135,135),(0,255,0),10)
                cv2.rectangle(img,(485,20),(485+135,135),(0,255,0),10)

                                
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8001, debug=True)
