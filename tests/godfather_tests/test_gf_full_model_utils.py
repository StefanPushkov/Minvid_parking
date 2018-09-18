import unittest

import cv2
import os

import godfather.gf_full_model_utils as fmu

class GFFullModelUtilsTest(unittest.TestCase):
    def test_get_right_contour(self):
        mask = cv2.imread(os.getcwd() + "/test_res/mask.png", 0)
        ret, thresh = cv2.threshold(mask, 127, 255, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print(fmu._get_right_contour(contours)[0])
        self.assertNotEqual(contours, [])
        self.assertTrue((fmu._get_right_contour(contours)[0] == [[460, 188]]).all())

if __name__ == "__main__":
    unittest.main()