# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

img1 = cv2.imread('./piNoir.jpg')          # queryImage
img2 = cv2.imread('./pi.jpg') # trainImage
# dtype:uint8
# imwrite after imread is unchange
# cv2 object is (hight,width,color(BGR)),Pillow object is RGB
akaze = cv2.AKAZE_create()


# find the keypoints and descriptors with SIFT
kp1, des1 = akaze.detectAndCompute(img1,None)
kp2, des2 = akaze.detectAndCompute(img2,None)

bf = cv2.BFMatcher()
# 特徴量ベクトル同士をBrute-Force＆KNNでマッチング
matches = bf.knnMatch(des1, des2, k=2)

# データを間引きする
ratio = 0.5
good = []
for m, n in matches:
    if m.distance < ratio * n.distance:
        good.append(m)
#        good.append(m)

# 特徴量をマッチング状況に応じてソートする
good = sorted(matches, key = lambda x : x[1].distance)

src_pts = np.float32([ kp1[m[0].queryIdx].pt for m in good ]).reshape(-1,1,2)
dst_pts = np.float32([ kp2[m[0].trainIdx].pt for m in good ]).reshape(-1,1,2)

M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
E = np.eye(3)
img1 = cv2.warpPerspective(img2,M,(1640,1232))


# create empty array 
img3 = np.empty_like(img1)

# 画像表示 (Ir - R) / (Ir + R)
#img3 = ((img1 - img2)/(img1 + img2)) *  255
img3[:,:,0] = (img1[:,:,0] + img2[:,:,0]) / (img1[:,:,0] -  img2[:,:,0]) * 255
img3[:,:,1] = (img1[:,:,1] + img2[:,:,1]) / (img1[:,:,1] -  img2[:,:,1]) * 255
img3[:,:,2] = (img1[:,:,2] + img2[:,:,2]) / (img1[:,:,2] -  img2[:,:,2]) * 255

# NDVI area
mask = 50
#print(np.count_nonzero(img3[:,:,2] >mask))

# binarization
img4 = img3[:,:,2]
ret,thresh1 = cv2.threshold(img4,mask,255,cv2.THRESH_BINARY)

# opening process
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

print(np.count_nonzero(opening > mask))

# confirm NDVI list
#import csv
#with open("stock.csv", "w") as f:
#    writer = csv.writer(f,lineterminator="\n")
#    writer.writerows(thresh1)

cv2.imshow('a',opening)
# キー押下で終了
cv2.waitKey(0)
cv2.destroyAllWindows()
