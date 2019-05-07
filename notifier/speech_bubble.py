import cv2
import pandas as pd
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import os


def read_info(file_name='images_info.csv'):
    return pd.read_csv(file_name, index_col='image')


def generate_image(images_info, image, message, font_path="OpenSans-Semibold.ttf"):
    left, top, right, bottom, anchor_x, anchor_y, r, g, b = images_info.loc[image].to_numpy()
    x, y = left + (right-left)//2, top + (bottom-top)//2
    img = cv2.imread(os.path.join('images', image))

    # main bubble
    cv2.ellipse(img, (x, y), ((right-left)//2, (bottom-top)//2), 0, 0, 360, (255, 255, 255), -1)

    # speech triangle
    triangle_cnt = np.array([(x, y), (x, top), (anchor_x, anchor_y)])
    cv2.drawContours(img, [triangle_cnt], 0, (255, 255, 255), -1)
    r, g, b = map(int, [r, g, b])

    # Text part
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    bubble_width, bubble_height = right-left, bottom-top
    w, h, font_size = 0, 0, 0
    font = ImageFont.truetype(font_path, font_size)
    for font_size in range(100, 10, -10):
        font = ImageFont.truetype(font_path, font_size)
        w, h = draw.textsize(message, font=font)
        if w < bubble_width-bubble_width*0.1 and h < bubble_height-bubble_height*0.1:
            break
    draw.text((left+(bubble_width-w)/2, top+(bubble_height-h)/2), message, font=font, fill=(b, g, r, 255))
    img = np.array(img_pil)
    return img


if __name__ == '__main__':
    images_info = read_info()
    img = generate_image(images_info, 'yellow_bird.jpg', 'Оставить документы в офисе')
    cv2.imshow('sfs', img)
    cv2.imwrite('tmp.png', img)
    cv2.waitKey()