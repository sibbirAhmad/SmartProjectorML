import cv2
import numpy as np
array = np.zeros((4,2),int)
counter = 0
def click(event,x,y,flag,params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame,(x,y),5,(255,0,0),-1)
        array[counter] = x,y
        counter = counter+1
#image = cv2.imread("../images/pers.png")
cap = cv2.VideoCapture("https://192.168.43.172:8080/video")


while True:
    _, frame = cap.read()
    if counter == 4:
        frame_height, frame_width, _ = frame.shape
        pts1 = np.float32([array[0], array[1],
                           array[2], array[3]])
        pts2 = np.float32([[0, 0], [frame_width, 0],
                           [0, frame_height], [frame_width, frame_height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        final = cv2.warpPerspective(frame, matrix, (frame_width, frame_height))
        cv2.imshow("Outup", final)
    cv2.namedWindow('Input')
    cv2.setMouseCallback('Input',click)
    cv2.imshow("Input",frame)
    cv2.waitKey(1)