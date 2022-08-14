import cv2
import numpy as np

image = cv2.imread("../images/pers.png")
#image = cv2.resize(image,(500,500))

pts1 = np.float32([[41,50],[350,43],[374,178],[64,274]])
pts2 = np.float32([[0,0],[462,0],[0,310],[462,310]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
final = cv2.warpPerspective(image,matrix,(462,310))
cv2.imshow("Outup",final)
cv2.imshow("Input",image)
cv2.waitKey(0)