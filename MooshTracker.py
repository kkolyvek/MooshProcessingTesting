"""
Moosh Systems 2021
"""

import os
import processImage
import exportImage
import cv2

def main():
    VID = "DJI_0001"
    BUCKBUNNY = "https://www.rmp-streaming.com/media/big-buck-bunny-360p.mp4"
    DRONE_STREAM = "rtmp://192.168.1.2/live/stream1"

    cap = cv2.VideoCapture(DRONE_STREAM)
    width, height, vid_fps = processImage.getParams(cap)

    # create pipe
    p = exportImage.createPipe("TWITCH", width, height, vid_fps)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("\nframe read failed")
            exportImage.destroyPipe(p)
            break

        # IMAGE PROCESSING OCCURS HERE
        processedFrame = processImage.MooshEdits(frame)

        # write to pipe
        exportImage.imageOut(p, processedFrame)
        cv2.imshow('debug view', processedFrame)

        if cv2.waitKey(1) == ord('q'):
            print('\nQuitting...')
            exportImage.destroyPipe(p)
            break

    exportImage.destroyPipe(p)

if __name__ == "__main__":
    main()
