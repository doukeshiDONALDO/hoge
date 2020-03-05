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
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good[:30], None, flags=2)

#cut       [hight(ue:shita)  , weight(hidari:migi)   ]
img2 = img2[667:915,735:980,:]
dst  =  dst[667:915,735:980,:]

# create empty array 
#img3 = np.empty_like(img1)
img3 = np.zeros(img2.shape)


#color mask
bgrLower = np.array([0,0,0])
bgrUpper = np.array([150,200,150])
img_mask = cv2.inRange(img2, bgrLower, bgrUpper)
img2 = cv2.bitwise_and(img2, img2, mask=img_mask)
#dst = cv2.bitwise_and(dst, dst, mask=img_mask)


print(np.count_nonzero(img3==0))

# NDVI process ((Ir - R) / (Ir + R) + 1 ) * 100
# if[divide by zero encountered in divid], x / 0 = 0(numpy)
img3[:,:,2] = ((dst[:,:,2] - img2[:,:,2]) / (dst[:,:,2] +  img2[:,:,2]) + 1 )* 100
img3[:,:,0] = img2[:,:,0]
img3[:,:,1] = img2[:,:,1]

print("img3: {}".format(np.count_nonzero(img3[:,:,2] > 200)))
#print("img2: {}".format(np.count_nonzero(img2[:,:,2] < 0)))


imgg = img3

#color mask
bgrLower = np.array([0,0,0])
bgrUpper = np.array([180,200,201])
img_mask = cv2.inRange(img3, bgrLower, bgrUpper)
result = cv2.bitwise_and(img3, img3, mask=img_mask)

img6 = result[:,:,2]
nsum = 0
for i in range(1,200):
    print('count:%s ' % i)
    print(np.count_nonzero(img6[:,:] == i))
    nsum += np.count_nonzero(img6[:,:] == i)
    print(nsum)
print("avarage: {}".format(nsum/255))




## NDVI area
#mask = 100
##print(np.count_nonzero(img3[:,:,2] >mask))
#
## binarization
#img4 = img3[:,:,2]
#ret,thresh1 = cv2.threshold(img4,mask,255,cv2.THRESH_BINARY)
#
## opening process
#kernel = np.ones((5,5),np.uint8)
#opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
#
#print(np.count_nonzero(opening > mask))
##img3[:,:,2] = img4
#
## confirm NDVI list
#import csv
#with open("stock.csv", "w") as f:
#    writer = csv.writer(f,lineterminator="\n")
#    writer.writerows(img6)
#
#cv2.imshow('a',img3)
#cv2.imshow('a',img6)
cv2.imwrite('/home/niki/hoge/fileupload/{}.png'.format("dst"),dst)
cv2.imwrite('/home/niki/hoge/fileupload/{}.png'.format("img2"),img2)
## キー押下で終了
#cv2.waitKey(0)
#cv2.destroyAllWindows()
