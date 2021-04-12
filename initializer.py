from util.TrackAndDetect import Frame
from default.coordinate_finder import get_box, get_line
from gui import qtWindow

import cv2


def frame_setup(frame):


    qtWindow()

    '''
    Region which we are detecting in and detection parameters
    '''
    
    confidence_threshold = qtWindow.form.doubleSpinBox.value() #confidence of detections
    sensitive_confidence_threshold = None #more sensitive confidence
    maxDetectFail = qtWindow.form.spinBox_4.value() #Number of frames before an object is no considered no longer to be in frame
    detection_interval = qtWindow.form.spinBox_3.value() #Number of frames object detection is carried out
    slower_detection = qtWindow.form.checkBox_4.isChecked() #Changes detection interval to one when no one is in the frame
    
    '''
    Tracking paramaeters (tracker used: csrt)
    '''
    maxTrackFail = qtWindow.form.spinBox_5.value() #Number of frames before the object is determined to have left the frame
    duplicate_object_threshold = qtWindow.form.doubleSpinBox_3.value() #Remove objects with overlap at this threshold


    '''
    Parameters to setup line for entry/exit point
    '''
    count_by_line = qtWindow.form.radioButton_5.isChecked()

    qtWindow.form.radioButton.isChecked()

    if count_by_line:
        if qtWindow.form.radioButton.isChecked():
            line_orientation = 'right'
            line_position = get_line('right')
        elif  qtWindow.form.radioButton_3.isChecked():
            line_orientation = 'left'
            line_position = get_line('left')
        elif  qtWindow.form.radioButton_2.isChecked():
            line_orientation = 'top'
            line_position = get_line('top')
        elif  qtWindow.form.radioButton_4.isChecked():
            line_orientation = 'bottom'
            line_position = get_line('bottom')
            
    else:
        line_orientation = None
        line_position = None

    '''
    Paramaters to setup a polygon for entry/exit point
    '''

    count_by_poly = qtWindow.form.radioButton_7.isChecked()
    show_poly = qtWindow.form.radioButton_7.isChecked()
    poly_outside = qtWindow.form.checkBox_3.isChecked()
    if count_by_poly:
        x,y,w,h = get_box()
        poly_points =  [(x,y+h),(x+w, y+h), (x+w,y), (x, y)]
    else:
        poly_points = None
    
    '''
    Tracking Range
    '''
    set_obj_range =  qtWindow.form.checkBox_2.isChecked()
    if set_obj_range:
        x,y,w,h = get_box()
        obj_range =  [(x,y+h),(x+w, y+h), (x+w,y), (x, y)]
        show_obj_range = False
    else:
        obj_range = None
        show_obj_range = False
    

    track_and_detect = Frame(frame, maxDetectFail, maxTrackFail, detection_interval, slower_detection, 
                            confidence_threshold, sensitive_confidence_threshold, duplicate_object_threshold,
                            line_orientation, line_position,
                            poly_points, show_poly,poly_outside,
                            obj_range, show_obj_range)
    
    return track_and_detect


    
    



