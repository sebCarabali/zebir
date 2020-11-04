import cv2 as cv
from . import utils
import numpy as np


def grab_image(stream=None):
    data = stream.read()
    image = np.asarray(bytearray(data), dtype=np.uint8)
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image


class ORBExtractor:

    def __init__(self, stream):
        self.image = grab_image(stream)

    def compute(self):
        orb = cv.ORB_create()
        kp = orb.detect(self.image, None)
        _, des = orb.compute(self.image, kp)
        return des
