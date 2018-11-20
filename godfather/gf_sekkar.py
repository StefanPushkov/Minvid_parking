# Class for processing images and returning answer as json


from config import CONFIG
import numpy as np
from godfather.gf_full_model_utils import car_seg_to_plate_and_corners, plates_seg_to_texts
from godfather.plate_frame_model import unet4
from godfather.plate_text_model import unet3
from json import dumps


class Sekkar():
    def __init__(self):
        self.load_nets()

    def load_nets(self):
        self.stage1 = unet4(image_rows=CONFIG.IMAGE_HEIGHT, image_cols=CONFIG.IMAGE_WIDTH)
        self.stage2 = unet3()

        self.stage1.load_weights(CONFIG.stage1_weights)
        self.stage2.load_weights(CONFIG.stage2_weights)

        # Initialization of nets. Instead stage1.predict() throws exception.
        self.stage1._make_predict_function()
        self.stage2._make_predict_function()

    # Convert (y, x) to (1, y, x, 1)
    def expand(self, image):
        assert(len(image.shape) == 2) #TODO remove assert, make test instead
        image = np.expand_dims(image, axis = 0)
        image = np.expand_dims(image, axis = 3)
        return image

    # Convert (1, y, x, 1) to (y, x)
    def squeeze(self, image):
        assert (len(image.shape) > 2)
        image = np.squeeze(image)
        return image

    # Convert from {'lb': [0, 0], 'rb': [0, 0], 'rt': [0, 0], 'lt': [0, 0]}
    # to "460,188;573,194;573,219;460,212"
    # for to send as json string
    def corners_to_string(self, corners):
        string = ''
        for i in ['lb', 'rb', 'rt', 'lt']:  # Order lb-rb-rt-lt is essential!
            point = corners[i]
            string += str(point[0]) + ',' + str(point[1]) + ';'
        string = string[:-1]

        return string

    # Processes image and returns json string.
    # Example: '{"status": 1, "number": "AER964", "frame": "514,215;627,219;626,241;513,236", "confidence": 100}'
    def predict(self, image):

        #time.sleep(1)
        #return '{"status": 1, "number": "AER964", "frame": "514,215;627,219;626,241;513,236", "confidence": 100}'

        image = image / 255.0

        image_exp = self.expand(image)

        mask_exp = self.stage1.predict(image_exp)
        mask = self.squeeze(mask_exp)

        plate, corners = car_seg_to_plate_and_corners(image, mask)

        plate_exp = self.expand(plate)

        plate_mask = self.stage2.predict(plate_exp)

        pred_texts = plates_seg_to_texts(plate_mask)

        pred_text = pred_texts[0] # Convert from ["text"] to "text" #TODO: change util
        pred_text = pred_text.replace('#', '')

        answer = {'status': 1, 'number':pred_text, 'frame': self.corners_to_string(corners), 'confidence': 100}
        answer = dumps(answer)

        return answer