import cv2
import mediapipe as mp
import serial
from math import atan2, pi
import HandMovementModule as hmm

# Initialize the Hand Detection module
hand_detector = hmm.HandDetector()

# Set up serial communication with Arduino
arduino = serial.Serial('/dev/tty.usbmodem11101', 9600)

cap = cv2.VideoCapture(0)

def finger_angle(lmList, finger_id):
    # Calculate the angle between the finger joints
    x1, y1 = lmList[finger_id][0], lmList[finger_id][1]
    x2, y2 = lmList[finger_id - 2][0], lmList[finger_id - 2][1]
    x3, y3 = lmList[finger_id - 3][0], lmList[finger_id - 3][1]

    angle = abs(atan2(y3 - y2, x3 - x2) - atan2(y1 - y2, x1 - x2))
    return int(angle * 180 / pi)  # Convert to degrees

while True:
    success, img = cap.read()

    # Detect hands
    hands, img = hand_detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand = hands[0]
        landmarks = hand["lmList"]

        # Get finger angles
        thumb_angle = finger_angle(landmarks, 4)
        index_angle = finger_angle(landmarks, 8)
        middle_angle = finger_angle(landmarks, 12)
        ring_angle = finger_angle(landmarks, 16)
        pinky_angle = finger_angle(landmarks, 20)
        print(thumb_angle -180)
        # Send finger angles to Arduino
        arduino.write(f"{thumb_angle-180},{index_angle},{middle_angle},{ring_angle},{pinky_angle}\n".encode())

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
