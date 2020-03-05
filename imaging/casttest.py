# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys
from sys import argv
import sqlite3
import subprocess

class QQ():
    def __init__(self):
        self.qtable = np.zeros((8,8))
        self.state = 0
        self.action = 0
        self.turn = 1
        self.trying = [0,0,0,0,0,0,0,0]




MIN_MATCH_COUNT = 10

#img1 = cv2.imread('./piNoir1.jpg')          # queryImage
#img2 = cv2.imread('./pi1.jpg') # trainImage

img1 = cv2.imread(sys.argv[1])          # noirImage
img2 = cv2.imread(sys.argv[2]) # normalImage


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
dst = cv2.warpPerspective(img1,M,(1640,1232))

# 対応する特徴点同士を描画
#img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good[:30], None, flags=2)

#ratate
height = img2.shape[0]
width = img2.shape[1]
center = (int(width/2), int(height/2))
angle = 0.0 # +hidari -migi
scale = 1.0
trans = cv2.getRotationMatrix2D(center, angle , scale)
dst = cv2.warpAffine(dst, trans, (width,height))
img2 = cv2.warpAffine(img2, trans, (width,height))


#cut       [hight(ue:shita)  , weight(hidari:migi)   ]
img2 = img2[655:908,750:995,:]
dst  =  dst[655:908,750:995,:]

# create empty array 
#img3 = np.empty_like(img1)
img3 = np.zeros(img2.shape)
a = np.zeros(img2.shape,dtype=np.float128)

## make color_mask
bgrLower = np.array([0,0,0])
bgrUpper = np.array([180,200,201])
img_mask = cv2.inRange(img2, bgrLower, bgrUpper)
imgg = cv2.bitwise_and(img2, img2, mask=img_mask)
#dst  = cv2.bitwise_and(dst, dst, mask=img_mask)


#print(np.count_nonzero(img3==0))

# NDVI process ((Ir - R) / (Ir + R) + 1 ) * 100
# if[divide by zero encountered in divid], x / 0 = 0(numpy)

a = dst[:,:,2].astype(np.float128) + img2[:,:,2].astype(np.float128)
b = dst[:,:,2].astype(np.float128) - img2[:,:,2].astype(np.float128)
c = (b / a + 1 ) * 100
img3[:,:,2] = c.astype(np.int64)
img3[:,:,0] = img2[:,:,0]
img3[:,:,1] = img2[:,:,1]





print(c)


print(img3[:,:,2])
