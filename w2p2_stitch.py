import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import math

VIDEO_PATH = "/Users/olivercho/Desktop/Programming/uavs@berkeley/example_videos/minecraft.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)
sift = cv2.SIFT_create(0, 3, 0.09, 10, 1.6)
frames = []

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    frames.append(frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()

# Downsample frames to every 30th frame and then to 1/4th the size
frames = frames[::30]
for i in range(len(frames)):
    frames[i] = cv2.resize(frames[i], (0, 0), fx=0.25, fy=0.25)

# Print out individual frames in a grid
num_cols = 4
num_rows = math.ceil(len(frames) / num_cols)
fig, axes = plt.subplots(num_rows, num_cols)
axes = axes.flatten()

for i, frame in enumerate(frames): # Print out individual frames in a grid
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    axes[i].imshow(frame)
    axes[i].axis("off")

for i in range(len(frames), len(axes)): # Hide unused subplots
    axes[i].axis("off")

plt.suptitle("Individual Frames", fontsize=16)
plt.tight_layout()



# Stitch frames into panorama
stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
status, panorama = stitcher.stitch(frames)

cv2.imshow("Stitched Panorama", panorama)

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("output/minecraft_stitched.png", panorama)