import cv2
import numpy as np

VIDEO_PATH = "/Users/olivercho/Desktop/Programming/uavs@berkeley/example_videos/minecraft.mp4"

"""
HOW DOES IT WORK

1. Detect keypoints in both images
2. Match keypoints between images  
3. Filter matches (ratio test)
4. Estimate homography (with RANSAC)
5. Warp first image to align with second
6. Composite images together
7. Repeat for all image pairs
"""

# Collect frames
cap = cv2.VideoCapture(VIDEO_PATH)
frames = []

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    frames.append(frame)

cap.release()

# Downsample frames to every 30th frame and then to 1/4th the size
frames = frames[::30]
for i in range(len(frames)):
    frames[i] = cv2.resize(frames[i], (0, 0), fx=0.25, fy=0.25)

# Apply SIFT to deteect keypoints in each frame
sift = cv2.SIFT_create(0, 3, 0.09, 10, 1.6)
bf = cv2.BFMatcher()

def stitch_images(image1, image2):
    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)

    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # ratio test to filter out good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 2)

    homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h1, w1 = image1.shape[:2]
    h2, w2 = image2.shape[:2]

    result = cv2.warpPerspective(image1, homography, (max(w1, w2), h1 + h2))
    result[0:h2, 0:w2] = image2

    return result

stitched_image = frames[0]
for i in range(1, len(frames)):
    stitched_image = stitch_images(stitched_image, frames[i])

cv2.imshow("Stitched Image", stitched_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("output/minecraft_SIFT_stitched.png", stitched_image)