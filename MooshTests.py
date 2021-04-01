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
    """
    Define process upon mouse actions
    Mouse left-click down: begin drawing, record initial points
    Mouse left-click up: finish drawing, record final points for rect
    Mouse move while drawing: show box to guide with drawing
    """
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

# GUI init
window_title = "MooshVision 2021"
cv2.namedWindow(window_title)
cv2.setMouseCallback(window_title, mouseClick)
sliderMax = 1000
cv2.createTrackbar("Contrast", window_title, 100, sliderMax, brightnessContrastSlider)
cv2.createTrackbar("Brightness", window_title, 500, sliderMax, brightnessContrastSlider)
brightnessContrastSlider(0)

# Tracker init
tracking = False
tracker = cv2.TrackerCSRT_create()

while fvs.running():
    frame = fvs.read()
    frame = imutils.resize(frame, width = int(3840/3))
    # frameCopy = frame # create a copy for a baseline

    #frame = processImage.brightnessContrast(frame, (currentContrast/100), (currentBrightness-500)/2)
    if keepRect == True:
        # process small window view
        frameHeight, frameWidth = fvs.params()
        subFrame = frame[y1:y2, x1:x2]
        subFrame = processImage.brightnessContrast(subFrame, (currentContrast/100),
                    (currentBrightness-500)/2)
        (processedSubFrame, x_init, y_init, w_init, h_init) = processImage.MooshEdits(subFrame)
        processedSubFrame = imutils.resize(processedSubFrame, width = 300)
        frame[50:int(subFrameHeight*300/subFrameWidth+50), 10:310] = processedSubFrame
    # update tracker (if applicable)
    if tracking == True:
        frame = processImage.updateTracker(frame, tracker)

    cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)
    processedFrame = frame
    cv2.imshow(window_title, processedFrame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        print("Quitting...")
        break
    if key == ord("c"):
        # Clear View
        keepRect = False
        #tracking = False
        cv2.imshow(window_title, processedFrame)
    if key == ord("t"):
        # Begin Tracking
        tracking = True
        boxExpanded = (int(x_init+x1-0.2*w_init), int(y_init+y1-0.2*h_init), int(1.4*w_init), int(1.4*h_init))
        tracker.init(frame, boxExpanded)
    fps.update()


fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx fps: {:.2f}".format(fps.fps())) # ~25 seems normal (no processing)

fvs.stop()
cv2.destroyAllWindows()
