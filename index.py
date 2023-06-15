import cv2
import mediapipe as mp
import pyautogui
import math

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

handDetector = mp.solutions.hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_x = 0
index_y = 0

while True:
    success, img = cap.read()
    if not success:
        raise Exception("Something went wrong!")

    img = cv2.flip(img, 1)

    height, width, _ = img.shape

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = handDetector.process(imgRGB)
    hands = results.multi_hand_landmarks

    if hands:
        for hand in hands:
            mpDraw.draw_landmarks(img, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                if id == 8:
                    cv2.circle(img, (x, y), 10, (0, 0, 255), 2)
                    index_x = int((x / width) * screen_width)
                    index_y = int((y / height) * screen_height)
                    pyautogui.moveTo(index_x, index_y, duration=0)
                if id == 4:
                    cv2.circle(img, (x, y), 10, (0, 0, 255), 2)
                    thumb_x = int((x / width) * screen_width)
                    thumb_y = int((y / height) * screen_height)
                    distance = math.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2)
                    if distance < 30:
                        pyautogui.click()

    cv2.imshow("Virtual Mouse", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break