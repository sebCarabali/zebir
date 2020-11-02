from imageretrival.imageprocessing.utils import from_json
from imageretrival.imageprocessing.featureextraction import ORBExtractor
import cv2 as cv


class HammingDistanceMatcher:

    def match(self, desc1, desc2):
        bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
        return bf.match(desc1, desc2)

    def get_matcher_value(self, desc1, desc2):
        total = min(desc1.shape[0], desc2.shape[0])
        matches = self.match(desc1, desc2)
        return len(matches) / total


class AbstractDuplicateFinder:
    def __init__(self, images):
        self.images = images

    def find_duplicates(self):
        pass


class ManualDuplicateFinder(AbstractDuplicateFinder):
    def __init__(self, images, image):
        AbstractDuplicateFinder.__init__(self, images)
        self.image = image

    def find_duplicates(self):
        desc = self._get_image_descriptor()
        matcher = HammingDistanceMatcher()
        res = []
        for img in self.images:
            mp = matcher.get_matcher_value(
                desc, from_json(img.descriptor.content))
            if mp > 0.70:
                res.append({
                    'img': img,
                    'probability': round(mp * 100)
                })
        return res

    def _get_image_descriptor(self):
        orb = ORBExtractor(self.image)
        return orb.compute()


class AutomaticDuplicateFinder(AbstractDuplicateFinder):

    def __init__(self, images):
        AbstractDuplicateFinder.__init__(self, images)

    def find_duplicates(self):
        matcher = HammingDistanceMatcher()
        res = []
        visited = [False] * len(self.images)
        has_duplicates = False
        for idx, img in enumerate(self.images):
            if not visited[idx]:
                for j in range(idx+1, len(self.images)):
                    if not visited[j]:
                        mp = matcher.get_matcher_value(
                            from_json(img.descriptor.content), from_json(self.images[j].descriptor.content))
                        if mp > 0.70:
                            has_duplicates = True
                            res.append({
                                'img': self.images[j],
                                'probability': round(mp * 100)
                            })
                            visited[j] = True
                if has_duplicates:
                    res.append({
                        'img': img,
                        'probability': 100
                    })
                visited[idx] = True
            has_duplicates = False
        return res
