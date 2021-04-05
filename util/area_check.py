'''
Checks to see if a person enters or leaves an area
'''
import numpy as np
import cv2

def draw_roi(frame,polygon,color=(0,255,255)):
    overlay = frame.copy()
    polygon = np.array([polygon], dtype=np.int32)
    cv2.fillPoly(overlay, polygon, color)
    alpha = 0.3
    output = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    return output


def get_roi_frame(current_frame,polygon):
    mask = np.zeros(current_frame.shape, dtype=np.uint8)
    polygon = np.array([polygon], dtype=np.int32)
    num_frame_channels = current_frame.shape[2]
    mask_ignore_color = (255,) * num_frame_channels
    cv2.fillPoly(mask, polygon, mask_ignore_color)
    masked_frame = cv2.bitwise_and(current_frame, mask)
    return masked_frame


def get_counting_line(line_orientation, frame_width, frame_height, line_position):

    line_orientations_list = ['top', 'bottom', 'left', 'right']
    if line_orientation not in line_orientations_list:
        raise Exception('Invalid line position specified (options: top, bottom, left, right)')

    if line_orientation == 'top':
        counting_line_y = round(line_position * frame_height)
        return [(0, counting_line_y), (frame_width, counting_line_y)]
    elif line_orientation == 'bottom':
        counting_line_y = round(line_position * frame_height)
        return [(0, counting_line_y), (frame_width, counting_line_y)]
    elif line_orientation == 'left':
        counting_line_x = round(line_position * frame_width)
        return [(counting_line_x, 0), (counting_line_x, frame_height)]
    elif line_orientation == 'right':
        counting_line_x = round(line_position * frame_width)
        return [(counting_line_x, 0), (counting_line_x, frame_height)]


def _pass(_type,l_point=0, c_line=0, o_line=0,c_point=0,f_point=0, r_polygon=0, o_polygon=0, _enter=0):
    
    if _type == 'line':
        if o_line == 'top':
            return l_point[1] < c_line[0][1]
        elif o_line == 'bottom':
            return l_point[1] > c_line[0][1]
        elif o_line == 'left':
            return l_point[0] < c_line[0][0]
        elif o_line == 'right':
            return l_point[0] > c_line[0][0]
    
    elif _type == 'polygon':
        if o_polygon ^ _enter:
            return r_polygon.contains(c_point) and not r_polygon.contains(f_point)
        else:
            return r_polygon.contains(f_point) and not r_polygon.contains(c_point)
    else:
        raise Exception('Invalid Type of polygon/line')






