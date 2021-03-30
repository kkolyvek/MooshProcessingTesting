"""
Moosh Systems 2021

Methods to process drone footage real-time
"""

import cv2
import numpy as np

def getParams(cap):
    """
    returns certain video parameters
    """
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    vid_fps = int(cap.get(cv2.CAP_PROP_FPS))

    return width, height, vid_fps

def MooshEdits(frame):
    """
    Executes following processes to 'frame':
    - Bilateral Filter: to smooth image while retaining edges
    - Convert RGB -> HSV: easier to to set filter limits with
    - Masking: filter colors to find edges
    - Convert HSV -> Grayscale: cv2.findContours requires grayscale
    - Find Contours: set contour thresholds and create contour
    """

    """
    mask_light = cv2.inRange(frame, (75,75,75), (255,255,255))
    mask_green = cv2.inRange(frame, (70,90,40), (95,120,60))
    #gaussian = cv2.GaussianBlur(frame, (5,5), cv2.BORDER_TRANSPARENT)
    #median = cv2.medianBlur(frame, 5)
    #edges = cv2.Canny(median, 100, 200)
    #weighted = cv2.addWeighted(frame, 1.5, median, -0.5, 0)
    mask = cv2.bitwise_or(mask_light, mask_green)
    filtered = cv2.bitwise_and(frame, frame, mask = mask)


    blur = cv2.bilateralFilter(frame, 5, 75, 75, cv2.BORDER_TRANSPARENT)
    # construct filters based on background color - shark is usually gray

    #hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    x, y, z = np.shape(frame)
    avg_H = int((blur[20,20,0] + blur[x-20,20,0] + blur[20,y-20,0] + blur[x-20,y-20,0])/4)
    avg_S = int((blur[20,20,1] + blur[x-20,20,1] + blur[20,y-20,1] + blur[x-20,y-20,1])/4)
    avg_V = int((blur[20,20,2] + blur[x-20,20,2] + blur[20,y-20,2] + blur[x-20,y-20,2])/4)
    print("BGR: " + str(avg_H) + ", " + str(avg_S) + ", " + str(avg_V))
    sens = 50 # green mask H sensitivity
    blur[20,20,0] = 180
    blur[20,20,1] = 255
    blur[20,20,2] = 255
    """

    #mask_gray = cv2.inRange(blur, (0,0,110), (180, 255, 255))
    mask_light = cv2.inRange(frame, (100,100,100), (255,255,255)) # mask out light reflections
    mask_green = cv2.inRange(frame, (70,90,40), (95,120,60)) # mask out green water
    mask = cv2.bitwise_or(mask_light, mask_green)
    filtered = cv2.bitwise_and(frame, frame, mask = mask)


    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
    gray_invert = cv2.bitwise_not(gray)

    #ret, thresh = cv2.threshold(gray_invert, 165, 255, cv2.THRESH_TOZERO)
    #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(gray_invert, contours, -1, (0,0,0), 1)


    processedFrame = cv2.cvtColor(gray_invert, cv2.COLOR_GRAY2BGR)
    return processedFrame

def brightnessContrast(img, alpha=1, beta=0):
    """
    Alters brightness and contrast of an image following:
    g(i,j) = alpha * f(i, j) + beta
    where alpha is understood to be contrast and beta is brightness
    """
    print('alpha' + str(alpha), beta)
    dummy = np.array([])
    return cv2.convertScaleAbs(img, dummy, alpha, beta)
