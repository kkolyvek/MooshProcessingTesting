"""
Moosh Systems 2021

Methods to process drone footage
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

    # Do processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret1, thresh1 = cv2.threshold(gray, 110, 255, cv2.THRESH_TRUNC)
    gray_invert = cv2.bitwise_not(thresh1)
    ret2, thresh2 = cv2.threshold(gray_invert, 160, 255, cv2.THRESH_TOZERO)
    contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    processedFrame = cv2.cvtColor(thresh2, cv2.COLOR_GRAY2BGR)


    # Final edits and return (bounding box)
    maxContour = [];
    for c in contours:
        if np.size(c) > np.size(maxContour):
            maxContour = c
    (x, y, w, h) = cv2.boundingRect(maxContour)
    cv2.rectangle(processedFrame, (x,y), (x+w,y+h), (0,255,0), 1)
    cv2.drawContours(processedFrame, contours, -1, (0,0,255), 1)
    return processedFrame, x, y, w, h

def brightnessContrast(img, alpha=1, beta=0):
    """
    Alters brightness and contrast of an image following:
    g(i,j) = alpha * f(i, j) + beta
    where alpha is understood to be contrast and beta is brightness
    """
    dummy = np.array([])
    return cv2.convertScaleAbs(img, dummy, alpha, beta)

def updateTracker(img, tracker):
    """
    updates tracker etc etc
    """
    (ret, boundingBox) = tracker.update(img)
    if ret == True:
        (x, y, w, h) = [int(v) for v in boundingBox]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    return img
