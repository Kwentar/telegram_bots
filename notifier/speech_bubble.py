import cv2
import pandas as pd
import numpy as np


def read_info(file_name='images_info.csv'):
    return pd.read_csv(file_name, index_col='image')

images_info = read_info()
left, top, right, bottom, anchor_x, anchor_y, r, g, b = images_info.loc['yellow_bird.jpg'].to_numpy()
x, y = left + (right-left)//2, top + (bottom-top)//2
img = cv2.imread('images/yellow_bird.jpg')
cv2.ellipse(img, (x, y), ((right-left)//2, (bottom-top)//2), 0, 0, 360, (255, 255, 255), -1)
cv2.rectangle(img, (left, top), (right, bottom), 255)

pt1 = (x, y)
pt2 = (x, top)
pt3 = anchor_x, anchor_y
triangle_cnt = np.array([pt1, pt2, pt3])

cv2.drawContours(img, [triangle_cnt], 0, (255, 255, 255), -1)
cv2.imshow('sfs', img)
cv2.waitKey()