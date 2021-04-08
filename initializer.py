from util.TrackAndDetect import Frame
from default.coordinate_finder import get_box
import cv2


def frame_setup(frame):


    '''
    Region which we are detecting in and detection parameters
    '''
    
    confidence_threshold = 0.1 #confidence of detections
    sensitive_confidence_threshold = 0.05 #more sensitive confidence
    maxDetectFail = 30 #Number of frames before an object is no considered no longer to be in frame
    detection_interval = 3 #Number of frames object detection is carried out
    slower_detection = True #Changes detection interval to one when no one is in the frame
    
    '''
    Tracking paramaeters (tracker used: csrt)
    '''
    maxTrackFail = 5 #Number of frames before the object is determined to have left the frame
    duplicate_object_threshold = 0.1 #Remove objects with overlap at this threshold


    '''
    Parameters to setup line for entry/exit point
    '''
    count_by_line = False
    if count_by_line:
        line_orientation = 'bottom'
        line_position = 0.1
    else:
        line_orientation = None
        line_position = None

    '''
    Paramaters to setup a polygon for entry/exit point
    '''

    count_by_poly = True
    show_poly = False
    poly_outside = True
    if count_by_poly:
        x,y,w,h = get_box()
        poly_points =  [(x,y+h),(x+w, y+h), (x+w,y), (x, y)]
    else:
        poly_points = None
    
    '''
    Tracking Range
    '''
    set_obj_range = True
    if set_obj_range:
        x,y,w,h = get_box()
        obj_range =  [(x,y+h),(x+w, y+h), (x+w,y), (x, y)]
        show_obj_range = True
    else:
        obj_range = None
        show_obj_range = False
    

    track_and_detect = Frame(frame, maxDetectFail, maxTrackFail, detection_interval, slower_detection, 
                            confidence_threshold, sensitive_confidence_threshold, duplicate_object_threshold,
                            line_orientation, line_position,
                            poly_points, show_poly,poly_outside,
                            obj_range, show_obj_range)
    
    return track_and_detect


    
    



