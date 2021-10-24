import cv2
import mediapipe as mp
import time
class handDetector():
    def __init__(self , mode = False, maxHands = 2, detectionCon = 0.5 , trackCon = 0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon 
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon,)
        self.mpDraw  = mp.solutions.drawing_utils
        self.tipid = [4,8,12,16,20]



    def findHands(self,img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)  
    #print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:

            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img


    def findpositions(self, img, handno=0, draw = True):
        self.lmlist = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handno]
            for id,lm in enumerate(myHand.landmark):

                h , w , c = img.shape
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                self.lmlist.append([id,cx,cy])
        return self.lmlist   

    def fingersup(self):
        fingers = []
        if self.lmlist[self.tipid[0]][1] < self.lmlist[self.tipid[0]-1][1]:
                fingers.append(1)
        else:
                fingers.append(0)

        
        for id in range(1,5):

            if self.lmlist[self.tipid[id]][2] < self.lmlist[self.tipid[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0) 
        return fingers                
   
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector  = handDetector()
    while True:
        sucess , img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findpositions(img)
        if len(lmList) !=0:
            print(lmList[8])
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime  = cTime
        cv2.putText(img , str(int(fps)), (10,70),   cv2.FONT_HERSHEY_PLAIN,   3,    (0,255,0),   3)      
        cv2.imshow("HandTracking" , img)
        cv2.waitKey(1)

 


if __name__ == "__main__":
               main()