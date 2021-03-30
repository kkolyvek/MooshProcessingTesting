"""
Processing Tests - Using Drone Video Files
March 2021
"""
import cv2
import imutils
from imutils.video import FPS
from FileVideoStreamEdits import FileVideoStream
import time
import processImage


drawing = False
keepRect = False
# Call-Back Functions
def mouseClick(event, x, y, flags, param):
    global x1, y1, x2, y2, drawing, keepRect, subFrame, subFrameHeight, subFrameWidth
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x1, y1 = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x2, y2 = x, y
        if x1 != x2 and y1 != y2:
            keepRect = True
            subFrameHeight = abs(y2-y1)
            subFrameWidth = abs(x2-x1)
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        #cv2.rectangle(frame, (x1, y1), (x, y), (0,0,0), 1, cv2.LINE_4)
        #cv2.imshow("processed frame", processedFrame)
        pass

def brightnessContrastSlider(contrast=0):
    global currentContrast, currentBrightness
    currentContrast = cv2.getTrackbarPos("Contrast", window_title)
    currentBrightness = cv2.getTrackbarPos("Brightness", window_title)

VID = "DJI_0004.MOV" # Video file name
fvs = FileVideoStream(VID).start()
time.sleep(1.0)
fps = FPS().start()

# GUI Init
window_title = "MooshVision 2021"
cv2.namedWindow(window_title)
cv2.setMouseCallback(window_title, mouseClick)
sliderMax = 1000
cv2.createTrackbar("Contrast", window_title, 100, sliderMax, brightnessContrastSlider)
cv2.createTrackbar("Brightness", window_title, 500, sliderMax, brightnessContrastSlider)
brightnessContrastSlider(0)

while fvs.running():
    frame = fvs.read()
    frame = imutils.resize(frame, width = int(3840/3))
    frameCopy = frame # create a copy for a baseline

    frame = processImage.brightnessContrast(frame, (currentContrast/100), (currentBrightness-500)/2)
    if keepRect == True:
        frameHeight, frameWidth = fvs.params()
        subFrame = frameCopy[y1:y2, x1:x2]
        processedSubFrame = processImage.MooshEdits(subFrame)
        processedSubFrame = imutils.resize(processedSubFrame, width = 200)
        frame[50:int(subFrameHeight*200/subFrameWidth+50), 10:210] = processedSubFrame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 1, cv2.LINE_4)


    cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
    processedFrame = frame
    cv2.imshow(window_title, processedFrame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        print("Quitting...")
        break
    if key == ord("c"):
        keepRect = False
        cv2.imshow(window_title, processedFrame)
    fps.update()


fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx fps: {:.2f}".format(fps.fps())) # ~25 seems normal (no processing)

fvs.stop()
cv2.destroyAllWindows()
