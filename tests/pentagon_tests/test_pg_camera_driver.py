import unittest

import cv2
import numpy as np

import os
import sys
# gets path of project directory
def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]
sys.path.append(get_base_dir_by_name('carplates_server'))


import pentagon.pg_camera_driver as CD
from config import CONFIG

class PGCameraDriverTest(unittest.TestCase):
    def test_generate_image_path(self):
        path = CD.PGCameraDriver.generate_image_path()  # path = CD.PGCameraDriver.generate_image_path()

        self.assertTrue(path.startswith(CONFIG.images_root_folder))
        self.assertEqual(path.split('.')[1], 'png')

        path2 = CD.PGCameraDriver.generate_image_path()
        self.assertNotEqual(path, path2)

    #@unittest.skip('Run only on production server where it is a camera')
    def test_get_image_by_ip_and_save(self):
        image, path = CD.PGCameraDriver().get_image_by_ip_and_save('192.168.60.9')

        self.assertTrue(os.path.isfile(path))

        nchannels = len(image.shape)
        self.assertTrue(nchannels == 2 or nchannels == 3)

        if nchannels == 2:
            self.assertTrue(np.all(image == cv2.imread(path, 0)))
        if nchannels == 3:
            self.assertTrue(np.all(image == cv2.imread(path, -1)))

if __name__ == "__main__":
    unittest.main()