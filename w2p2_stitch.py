import cv2
import numpy as np
import os

VIDEO_PATH = "/Users/olivercho/Desktop/Programming/uavs@berkeley/example_videos/beach.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)
sift = cv2.SIFT_create(0, 3, 0.09, 10, 1.6)

frame_count = 0
while True:
    ret, frame = cap.read()
    
    # Downsample logic with modular arithmetic
    if frame_count % 10 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = sift.detectAndCompute(gray, None)
        frame = cv2.drawKeypoints(frame, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow("Frame with SIFT keypoints", frame)

    frame_count += 1

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print(frames)