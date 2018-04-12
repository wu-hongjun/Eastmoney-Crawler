# Hongjun Wu
# 20180207
# A small test on OpenCV and python.
# It can detect a T-REX and a tree from an image.

# Import Statement
import cv2
import numpy as np

# Process original image
image_background = cv2.imread('bg.png')
image_background2 = cv2.cvtColor(image_background, cv2.COLOR_BGR2GRAY)

# Declare object
t_rex = cv2.imread('trex.png', 0)
plant = cv2.imread('plant.png', 0)

# Identify shape
w, h = t_rex.shape[::-1]
tw, th = plant.shape[::-1]

res = cv2.matchTemplate(image_background2, t_rex, cv2.TM_CCOEFF_NORMED)
res2 = cv2.matchTemplate(image_background2, plant, cv2.TM_CCOEFF_NORMED)

# Determine threshold
threshold = 0.8

# Display and find where objects are
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(image_background, pt, (pt[0]+w, pt[1]+h), (255, 0, 255), 2)

loc = np.where(res2 >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(image_background, pt, (pt[0]+tw, pt[1]+th), (255, 0, 255), 2)

# Show window
cv2.imshow('Detected!', image_background)
cv2.waitKey(0)
cv2.destroyAllWindows()

