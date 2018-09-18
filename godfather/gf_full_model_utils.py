# This is a set of utils used in prediction. Simple classical algorithms only


import numpy as np
import cv2 as cv
import cv2 as cv2

# from contours given selects the one the most likely
# being the carplate
def _get_right_contour(contours):
    contours2 = []
    for cnt in contours:
        if cv2.contourArea(cnt) < 1000:
            continue
        else:
            contours2.append(cnt)
    max_m = 0
    max_i = 0

    if len(contours2) == 0:
        return None

    for i in range(len(contours2)):
        M = cv2.moments(contours2[i])
        m = M['m01'] / M['m00']
        if m > max_m:
            max_m = m
            max_i = i

    return contours2[max_i]


# function y=x /
def _is_second_above_y_eq_x(first, second):
    x0, y0 = first
    x1, y1 = second
    return (y1 - y0) > (x1-x0)


# function y=-x \
def _is_second_above_y_eq_minus_x(first, second):
    x0, y0 = first
    x1, y1 = second
    return (y0 - y1) < (x1-x0)

# finds positions of corners of carplate and returns them as dictionary
# {'lb': [0, 0], 'rb': [0, 0], 'rt': [0, 0], 'lt': [0, 0]}
# mind the right order: lb-rb-rt-lt
def _find_corners(mask):
    ret, thresh = cv.threshold(mask, 127, 255, 0)
    im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    corners = {'lb': [1000, 1000], 'rb': [0, 1000], 'rt': [0, 0], 'lt': [1000, 0]}  #each point is [x,y]

    right_contour = _get_right_contour(contours)

    if right_contour is None:
        return {'lb': [0, 200], 'rb': [200, 200], 'rt': [0, 0], 'lt': [200, 0]} #TODO give more logical value

    for point in right_contour:
        point = point[0]

        if (_is_second_above_y_eq_x(corners['lt'], point)):
            corners['lt'] = point
        if (_is_second_above_y_eq_x(point, corners['rb'])):
            corners['rb'] = point
        if (_is_second_above_y_eq_minus_x(corners['rt'], point)):
            corners['rt'] = point
        if (_is_second_above_y_eq_minus_x(point, corners['lb'])):
            corners['lb'] = point

    return corners



# applies perspective transform to src image and returns plate as np.array (40,200) and corners
def car_seg_to_plate_and_corners(image, mask):
    if mask.dtype == 'float32': # mask is float32 with range 0..1.0 after prediction
        mask = (mask*255).astype('uint8')
    corners = _find_corners(mask)

    i = 0
    pts = np.array([[0, 0], [0, 0], [0, 0], [0, 0]], dtype='float32')
    for point in corners:
        point = corners[point]
        pts[i] = point
        i = i + 1

    pts2 = np.array([[0, 0], [200, 0], [200, 40], [0, 40]], dtype='float32')

    M = cv2.getPerspectiveTransform(pts, pts2)
    plate = cv2.warpPerspective(image, M, (300, 300))
    plate = plate[:40, :200]

    return plate, corners

# same as "car_seg_to_plate_and_corners", but returns only plate
def car_seg_to_plate(image, mask):
    plate, corners = car_seg_to_plate_and_corners(image, mask)
    return plate

# 37 symbols
_labels = ['#', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
          'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
          'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Converts segmentation mask into text string
def plates_seg_to_texts(preds):
    numbers = []

    avg = np.average(preds, axis=1)  # preds (N, y, x, channels) -> (N, x, channels)
    levels = np.argmax(avg, axis=2)  # preds (N, x, channels_binary_vector) -> (N, x, channels_integer)
    for level in levels:  # level is (x, channels_integer)
        # chars is a list [[char_idx, number_in_row], ...]
        #  example: "###001" -> [[0,3],[1,2],[2,1]]
        chars = [[level[0], 1]]
        j = 0
        for i in range(len(level) - 1):
            if level[i + 1] == level[i]:
                chars[j][1] += 1
            else:
                j += 1
                chars.append([level[i + 1], 1])
        text = ''
        for char in chars:
            if char[1] >= 10:
                text += _labels[char[0]]
            if char[1] >= 40:
                text += _labels[char[0]]
            if char[1] >= 70:
                text += _labels[char[0]]
        numbers.append(text)
        # print(chars)
    return numbers

if __name__ == "__main__":
    print(_is_second_above_y_eq_x([1, 1], [2, 2.1])) #True
    print(_is_second_above_y_eq_x([100, 100], [1000, 1000])) #False