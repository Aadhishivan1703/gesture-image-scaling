# Gesture Controlled Image Scaling using OpenCV and cvzone

import cv2
from cvzone.HandTrackingModule import HandDetector

# Initialize video capture and set resolution
cap = cv2.VideoCapture(0)
cap.set(3, 2160)
cap.set(4, 1080)

# Initialize HandDetector with a confidence threshold
detector = HandDetector(detectionCon=0.5)

# Variables for scaling and image placement
scale = 0
cx, cy = 0, 0
startDist = None

# Load the image to be scaled
img1 = cv2.imread("/Users/aadhishivan/Downloads/mqp1144-250x250h.jpeg.webp")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip for mirror view

    # Detect hands
    hands, img = detector.findHands(img)

    # Check if two hands are detected
    if len(hands) == 2:
        # Check if both hands show index and middle fingers (peace sign)
        if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:

            # Get initial distance between the hands
            if startDist is None:
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
                startDist = length

            # Measure new distance and calculate scale
            length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
            scale = int((length - startDist) // 2)
            cx, cy = info[4:]
            print(f"Scale: {scale}")
    else:
        startDist = None

    # Try applying the scaling and placing the image
    try:
        h1, w1, _ = img1.shape
        nh, nw = ((h1 + scale) // 2) * 2, ((w1 + scale) // 2) * 2
        resized_img1 = cv2.resize(img1, (nw, nh))
        img[cy - nh // 2: cy + nh // 2, cx - nw // 2: cx + nw // 2] = resized_img1
    except:
        pass

    # Display the result
    cv2.imshow("Gesture Controlled Image Scaling", img)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
