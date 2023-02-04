#importing some module
import cv2
import time
import numpy as np
import HandTrackingModule as htm  
import math

############################################################
        #importing pycaw module to get volume controls

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

############################################################

wCam , hCam = 400, 500   # oriantation of cam

cap = cv2.VideoCapture(0)  #our video object
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7) #object for HandTrackingModule




        ##volume controls##
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar=400
volPer=0




while True:
    success, img = cap.read()
    img = detector.findHands(img)    #finding(detecting) hands
    lmList = detector.findPosition(img , draw=True) #listing the position of hand
    

    #if some points are detected in lmList
    if len(lmList) !=0:        
        x1 ,y1 = lmList[4][1], lmList[4][2]
        x2 ,y2 = lmList[8][1], lmList[8][2]
        cx ,cy = (x1 +x2 )//2 , (y1 + y2)//2
        #draw circle at point 4 and 8 
        cv2.circle(img,(x1 ,y1),15,(255,0,255), cv2.FILLED) 
        cv2.circle(img,(x2 ,y2),15,(255,0,255), cv2.FILLED)
    
        cv2.line(img,(x1,y1),(x2,y2),(200,100,50),3)   #draw the line b/w 4 and 8 
        cv2.circle(img,(cx ,cy),15,(0,127,255), cv2.FILLED) #draw circle in mid of line

        #to know length b/w line
        length = math.hypot(x2-x1,y2-y1)
        print(length)



    ############################################################
        #our hand range from 50 to 300
        #volume range is from  -65 to 0
        #converting the range using numpy module

        vol = np.interp(length,[50,300],[minVol , maxVol])
        volBar = np.interp(length,[50,300],[400 , 150])
        volPer = np.interp(length,[50,300],[0 , 100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)
    ###########################################################


        if length <50:
            cv2.circle(img,(cx ,cy),15,(0,0,0), cv2.FILLED)



    #inserting the rectangular bar to show volume
    cv2.rectangle(img ,(50,150),(85,400),(255,255,255),3)
    cv2.rectangle(img ,(50,int(volBar)),(85,400),(0, 255 ,255),cv2.FILLED)

    cv2.putText(img , f' {int(volPer)} %',(40,450), cv2.FONT_HERSHEY_PLAIN,1,(0,250,0),2)



    #showing fps time
    cTime=time.time()
    fps= 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img , f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_PLAIN,1, (0,0,255),2)



    cv2.imshow("Img", img)
    cv2.waitKey(1)