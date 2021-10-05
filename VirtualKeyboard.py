import cv2
import Handtracking as htm
import math
from time import sleep
from pynput.keyboard  import Controller
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

finaltext = ""

keyboard = Controller()
detector = htm.handDetector(detectionCon = 0.8)

keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

def drawall(img , buttonlist):

    for button in buttonlist:
        x,y = button.pos
        w, h = button.size
        cv2.rectangle(img,button.pos ,(x+w , y+h), (255, 0 ,255),cv2.FILLED)
        cv2.putText(img, button.text , (x+15 , y+65),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),3)
    return img    


class Button():
    def __init__(self , pos , text, size = [80,80]):

        self.pos = pos
        self.text = text
        self.size = size
        
buttonlist = []

for i in range (len(keys)):
        for j, key in enumerate(keys[i]):
          buttonlist.append(Button([100*j+30 , 100*i+30],key))   

while True:

    sucess , img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findpositions(img)
   
    img = drawall(img , buttonlist)
    
    if lmlist :
        for button in buttonlist:
            x,y = button.pos
            w,h = button.size
            
            if x < lmlist[8][1 ] < x+w and y <lmlist[8][2] < y+h:
                cv2.rectangle(img,button.pos ,(x+w , y+h), (0, 0 ,255),cv2.FILLED)
                cv2.putText(img, button.text , (x+15 , y+65),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),3) 
                x1,y1 = lmlist[8][1] , lmlist[8][2]
                x2,y2 = lmlist[12][1] , lmlist[12][2]
                
                length = math.hypot(x1-x2,y1-y2)
                        

                if length<30:

                    keyboard.press(button.text)
                    cv2.rectangle(img,button.pos ,(x+w , y+h), (255, 0 ,0),cv2.FILLED)
                    cv2.putText(img, button.text , (x+15 , y+65),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),3) 
                    finaltext += button.text
                    #print(finaltext) 
                    sleep(0.20)
    cv2.rectangle(img ,(50,350),(700,450), (255, 0 ,0),cv2.FILLED)
    cv2.putText(img, finaltext , (60 , 425),cv2.FONT_HERSHEY_PLAIN,5,(255,255,255),5)                             
    cv2.imshow("key",img)
    cv2.waitKey(1)