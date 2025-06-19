import cv2
from cvzone.HandTrackingModule import HandDetector

cap=cv2.VideoCapture(0)
#resolution
cap.set(3,2160)
cap.set(4,1080)
detect=HandDetector(detectionCon=0.5)
scale=0
cy,cx=0,0

while True:
    success,img=cap.read()
    #flipping the camera 
    img = cv2.flip(img, 1)  
    hands,img=detect.findHands(img)
    img1=cv2.imread("/Users/aadhishivan/Downloads/mqp1144-250x250h.jpeg.webp")

    if len(hands)==2:

        if detect.fingersUp(hands[0])==[1,1,0,0,0] and detect.fingersUp(hands[1])==[1,1,0,0,0]:

            if startDist is None:

                length,info,img=detect.findDistance(hands[0]["center"],hands[1]["center"],img)
                startDist=length

            length,info,img=detect.findDistance(hands[0]["center"],hands[1]["center"],img)
            scale=int((length-startDist)//2)
            cx,cy=info[4:]
            print( scale)
    else:
        startDist=None

    try:
        h1,w1,_=img1.shape
        nh,nw=((h1+scale)//2)*2,((w1+scale)//2)*2 
        img1=cv2.resize(img1,(nw,nh))
        img[cy-nh//2:cy+nh//2,cx-nw//2:cx+nw//2]=img1
    except:
        pass

    cv2.imshow("Gesture Controlled Image Scaling",img)
    if cv2.waitKey(1) & 0xFF == ord('q'): #exit by pressing 'q'
        break

cap.release()
cv2.destroyAllWindows()
