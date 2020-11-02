import cv2 as cv
from . import utils

from .grabimage import grab_image

class ORBExtractor:

    def __init__(self, stream):
        self.image = grab_image(stream)
    
    def compute(self):
        orb = cv.ORB_create()
        kp = orb.detect(self.image,None)
        _ , des = orb.compute(self.image, kp)
        return des

    def to_json(self, des):
        return utils.to_json(des)
