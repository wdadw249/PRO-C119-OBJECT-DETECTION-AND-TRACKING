import cv2
import time
import math


p1 = 530
p2 = 300

xs = []
ys = []

vid = cv2.VideoCapture("footvolleyball.mp4")
tracker = cv2.TrackerCSRT_create()

ret, frame = vid.read()

bbox = cv2.selectROI("Initiating..",frame,False)
tracker.init(frame,bbox)

def drawBox(img, boundingBox):
    x = int(boundingBox[0])
    y = int(boundingBox[1])
    width = int(boundingBox[2])
    height = int(boundingBox[3])
    cv2.putText(img,"Tracking..",(70,90),cv2.FONT_HERSHEY_COMPLEX_SMALL,fontScale=0.5, thickness=1, color=(0,0,255))
    cv2.rectangle(img,(x,y),(x+width,y+height), (0,0,255),4)

def goalTracking(img,boundingBox):
    x,y,w,h = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    c1 = x + int(w/2)
    c2 = y + int(h/2)
    cv2.circle(img,(c1,c2),2,(0,0,255),5)

    cv2.circle(img,(int(p1),int(p2)),2,(0,255,0),3)
    dist = math.sqrt(((c1-p1)**2) + (c2-p2)**2)
    print(dist)

    if(dist<=20):
        cv2.putText(img,"Goal",(300,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

    xs.append(c1)
    ys.append(c2)

    for i in range(len(xs)-1):
        cv2.circle(img,(xs[i],ys[i]),2,(0,0,255),5)

while True:
    bool, frame = vid.read()
    success,bbox = tracker.update(frame)
    if success:
        drawBox(frame,bbox)
    else:
        error = "We lost the object"
        cv2.putText(frame, error, (70,90),color=(0,0,255), fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,fontScale=0.5, thickness=1)
    
    goalTracking(frame,bbox)
    cv2.imshow("soccer", frame)

    if cv2.waitKey(25) == 32:
        break

vid.release()
cv2.destroyAllWindows()