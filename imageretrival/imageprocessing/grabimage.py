import numpy as np
import cv2 as cv

def grab_image(stream=None):
    data = stream.read()
    image = np.asarray(bytearray(data), dtype=np.uint8)
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image