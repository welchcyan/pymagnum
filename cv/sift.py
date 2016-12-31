import numpy as np
import cv2
from matplotlib import pyplot as plt

# read image
img = cv2.imread('/Users/chenw13/Pictures/cxyxt/pic140.JPG',cv2.IMREAD_COLOR)
img2 = cv2.imread('/Users/chenw13/Pictures/cxyxt/pic146.JPG',cv2.IMREAD_COLOR)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

#SIFT
detector = cv2.xfeatures2d.SIFT_create()
# keypoints = detector.detect(gray,None)

kp1, des1 = detector.detectAndCompute(gray,None)
kp2, des2 = detector.detectAndCompute(gray2,None)

# img = cv2.drawKeypoints(gray,keypoints, img)
# cv2.imshow('test',img);

bf = cv2.BFMatcher()

# Match descriptors.
matches = bf.knnMatch(des1,des2, k=2)

# Sort them in the order of their distance.
good = []
for m,n in matches:
    if m.distance < 0.75 * n.distance:
        good.append([m])

# Draw first 10 matches.
img3 = cv2.drawMatchesKnn(img,kp1,img2,kp2,good, img, flags=2)

plt.imshow(img3),plt.show()
