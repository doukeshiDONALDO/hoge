# -*- coding: utf-8 -*-


import cv2
import numpy as np

image = cv2.imread('./pi.jpg') # ファイル読み込み

# BGRでの色抽出
bgrLower = np.array([50, 50, 150])    # 抽出する色の下限(BGR)
bgrUpper = np.array([100, 100, 255])    # 抽出する色の上限(BGR)
img_mask = cv2.inRange(image, bgrLower, bgrUpper) # BGRからマスクを作成
result = cv2.bitwise_and(image, image, mask=img_mask) # 元画像とマスクを合成

cv2.imshow('a',result)


# キー押下で終了
cv2.waitKey(0)
cv2.destroyAllWindows()

