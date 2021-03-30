"""
ML Trainer - March 2021

"""
import os
import cv2
import numpy as np
import time

folder = r"D:\koppi_training"
#print(os.listdir(folder))

for filename in os.listdir(folder):
    img = cv2.imread(os.path.join(folder, filename))
    height,width,z = np.shape(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_invert = cv2.bitwise_not(gray)
    ret, thresh = cv2.threshold(gray_invert, 175, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, contours, -1, (0,255,0), 3)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(gray, (x,y), (x+w, y+h), (0,255,0), 2)

    resized = cv2.resize(gray, (int(width*0.2),int(height*0.2)))
    cv2.imshow("pic", resized)


    key = cv2.waitKey(0)
    if key == ord('q'):
        print("Quitting...")
        cv2.destroyAllWindows
        break

    cv2.destroyAllWindows
