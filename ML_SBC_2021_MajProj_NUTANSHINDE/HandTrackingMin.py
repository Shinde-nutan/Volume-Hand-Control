#importing some modules
import cv2 
import mediapipe as mp
import time
from mediapipe.python.solutions import drawing_utils



cap = cv2.VideoCapture(0) #our video object

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = drawing_utils #to draw lines b/w the points

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
       
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #sending rgb image to our object 
    results = hands.process(imgRGB)
    

    


    #checking multiple hands and extracting them one by one
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):   #knowing the position of landmarks 
                
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
               
                cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)


    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime


    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)   #showing frame rates on screen

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    