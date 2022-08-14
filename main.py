import cv2
import mediapipe as mp
import pyautogui
from pygrabber.dshow_graph import FilterGraph


graph = FilterGraph()
print(graph.get_input_devices())# list of camera device
try:
    device =graph.get_input_devices().index("DroidCam Source 3")
except ValueError as e:
 device = graph.get_input_devices().index("HP Truevision HD") #use default camera if the name of the camera that I want to use is not in my list
#"https://192.168.43.172:8080/video"
cap = cv2.VideoCapture("https://192.168.43.172:8080/video")

hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
index_y = 0

screen_width, screen_height = pyautogui.size()
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Todo : 1 means y axis flip
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    # Todo : Drawing hands
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x  # Radion of outer screen and frame
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)
                    print(index_x,index_y)
                    #pyautogui.sleep(0.1)
                if id == 4:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    #thumb_x = screen_width / frame_width * x  # Radion of outer screen and frame
                    thumb_y = screen_height / frame_height * y
                    #print(abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 51:
                       print("Clicked")
                       #pyautogui.click()
                       #pyautogui.sleep(1)

    cv2.imshow("Virtual Mouse", frame)
    key = cv2.waitKey(1)
    if key == 27:

        break




