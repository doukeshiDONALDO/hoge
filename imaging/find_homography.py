# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10

img1 = cv2.imread('./normal.png',0)          # queryImage
img2 = cv2.imread('./ir.png',0) # trainImage

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
        good.append([m])

# 特徴量をマッチング状況に応じてソートする
good = sorted(matches, key = lambda x : x[1].distance)

src_pts = np.float32([ kp1[m[0].queryIdx].pt for m in good ]).reshape(-1,1,2)
dst_pts = np.float32([ kp2[m[0].trainIdx].pt for m in good ]).reshape(-1,1,2)

M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
E = np.eye(3)
dst = cv2.warpPerspective(img1,M,(640,480))

# 画像表示
cv2.imshow('img', dst)

# キー押下で終了
cv2.waitKey(0)
cv2.destroyAllWindows()
