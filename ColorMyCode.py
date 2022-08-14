import cv2
import numpy as np
import pyautogui

cap = cv2.VideoCapture("https://192.168.43.172:8080/video")

kernel = np.ones((5,5),np.uint8)
noiseth = 50 # Noise image size



def nothing(x):
    print(x)
    pass


cv2.namedWindow("Trackbars")
cv2.createTrackbar("X", "Trackbars", 0, 1360, nothing)
cv2.createTrackbar("Y", "Trackbars", 0, 760, nothing)
screen_width, screen_height = pyautogui.size()
x = 0
y= 0
def mapRange(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))
while True:
    _, frame = cap.read()
    #frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    _x = cv2.getTrackbarPos("X", "Trackbars")
    _y = cv2.getTrackbarPos("Y", "Trackbars")
    # lower_blue = np.array([12, 0, 248])
    # upper_blue = np.array([140, 137, 255])
    # [[0, 0, 92], [179, 255, 255]] [Mobile
    lower_blue = np.array([0, 74, 174])
    upper_blue = np.array([179, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours and cv2.contourArea(max(contours,key = cv2.contourArea)) > noiseth:
        c = max(contours, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        if x > 0 and y > 0:
            aspect_ratio = float(w) / h
            index_x = screen_width / frame_width * x  # Radion of outer screen and frame
            index_y = screen_height / frame_height * y
            cv2.circle(img=frame, center=(x+10, y+10), radius=10, color=(0, 255, 255))
            m_x = mapRange(x,226,380,0,1360)
            m_y = mapRange(y,115,315,0,760)
            if m_x>0 and m_y>0:
                pyautogui.moveTo(m_x, m_y)

            # pyautogui.moveTo(m_x, m_y)
            #pyautogui.moveTo(index_x, index_y)
            #print(m_x, m_y)
            # print(aspect_ratio)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
            # cv2.circle(frame, maxLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)
            #cv2.circle(frame, maxLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)
            #cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
    #else:
        #print("Small Size")

    # result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    # cv2.imshow("result", result)

    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == ord('x'):
        print("X ",x)

    if key == ord('y'):
        print("Y ",y)


cap.release()
cv2.destroyAllWindows()
