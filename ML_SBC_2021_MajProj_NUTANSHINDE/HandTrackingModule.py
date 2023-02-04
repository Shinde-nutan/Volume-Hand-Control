#importing some modules
import cv2 
import mediapipe as mp
import time

from mediapipe.python.solutions import drawing_utils

class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

       


        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw = drawing_utils #to draw lines b/w the points


    def findHands(self,img , draw=True):
    
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #sending rgb image to our object 
        self.results = self.hands.process(imgRGB)
        

        


        #checking multiple hands and extracting them one by one
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return(img)

    def findPosition( self, img, handNo=0, draw=True):
        lmList =[]
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]


            for id, lm in enumerate(myHand.landmark):   #knowing the position of landmarks 
                    
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
               #print(id,cx,cy)
                lmList.append([id,cx,cy])
                
                if draw:
                    cv2.circle(img,(cx,cy),7,(200,100,50),cv2.FILLED)
        return (lmList)

        

   

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0) #our video object
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) !=0:

            print(lmList[4])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (181,255,78), 3)   #showing frame rates on screen

        cv2.imshow("Image", img)
        cv2.waitKey(1)
    




if __name__=="__main__":
    main()