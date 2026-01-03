import cv2
import numpy as np
import os

IMAGE_DIRECTORY = "/Users/olivercho/Desktop/Programming/uavs@berkeley/example_images"

for index, image in enumerate(os.listdir(IMAGE_DIRECTORY)):
    print(f"{index}: {image}")

print("=" * 50)
selection_index = int(input("Select an image by index: "))
print("=" * 50)

IMAGE_PATH = os.path.join(IMAGE_DIRECTORY, os.listdir(IMAGE_DIRECTORY)[selection_index])
print(IMAGE_PATH)

img = cv2.imread(IMAGE_PATH)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Display the image
cv2.imshow("Color Me Impressed", img)

cv2.waitKey(0)
cv2.destroyAllWindows()