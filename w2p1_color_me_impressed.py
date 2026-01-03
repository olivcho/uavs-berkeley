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

cv2.imshow("Original", img)

img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

LOWER_BOUND = np.array([0, 40, 80])
UPPER_BOUND = np.array([25, 170, 255])

mask = cv2.inRange(img, LOWER_BOUND, UPPER_BOUND)
cv2.imshow("Mask", mask)

# Print center of mass of the result
M = cv2.moments(mask)
center_of_mass = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))
print(f"Center of object: {center_of_mass}")

result = cv2.bitwise_and(img, img, mask=mask)
result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
cv2.circle(result, center_of_mass, 10, (0, 0, 255), -1)
cv2.imshow("Result", result)

cv2.waitKey(0)
cv2.destroyAllWindows()