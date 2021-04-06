import cv2
from collections import OrderedDict
import time

from .objects import add_new_objects
from .area_check import get_roi_frame, draw_roi
from .area_check import get_counting_line, _pass
from .bbox import _centroid
from .send_request import send_requests


from shapely.geometry.polygon import Polygon
from shapely.geometry import Point

class Frame:

    def __init__(self, currentframe, maxDetectionFail, maxTrackingFail, detection_interval,
                detectEveryFrame, confidenceThreshold, sensConfidenceThreshold,
                dupConfidenceThreshold, line_orientation, line_position,
                counting_region, show_counting_region, counting_region_out, 
                object_range, show_object_range):
    
        '''
        Initial Variables for for class for tracking and detection
        '''
        self.frame = currentframe
        self.frame_height, self.frame_width, _ = self.frame.shape
        self.frame_count = 0
        self.frame_rate_processing = 0
        self.person_in = 0
        self.person_out = 0
        self.objects = OrderedDict()
        self.types_counts = OrderedDict()
        self.bounding_boxes = []
        self.classes = []
        self.confidences = []
    
        '''
        Thresholds
        '''
        self.maxDetectionFail = maxDetectionFail
        self.maxTrackingFail = maxTrackingFail
        self.dupConfidenceThreshold = dupConfidenceThreshold
        self.sensConfidenceThreshold = sensConfidenceThreshold
        self.confidenceThreshold = confidenceThreshold
        self.detection_interval = detection_interval
        
        self.region = Polygon([(0, 0), (self.frame_width, 0), (self.frame_width, self.frame_height), (0, self.frame_height)])

        '''
        Check object passes line
        '''
        self.line_orientation = line_orientation
        self.line_position = line_position
        self.counting_line = None if line_orientation == None else get_counting_line(self.line_orientation, self.frame_width, self.frame_height, self.line_position)

        '''
        Check object passes a region
        '''
        self.counting_region = counting_region
        self.counting_poly = Polygon(self.counting_region) if counting_region else None
        self.counting_region_out = counting_region_out
        self.object_range = object_range if object_range else None
        self.object_range_poly = Polygon(object_range) if object_range else None
        

        '''
        Time parameters
        '''
        self.time_start = time.time()
        self.time_send = 0
        self.time_end = 0
        self.mask_off_enter = 0
        self.mask_off_leave = 0
        self.mask_on_enter = 0
        self.mask_off_enter = 0

        '''
        Visualization Parameters
        '''
        self.show_counting = show_counting_region
        self.show_object_range = show_object_range
        self.roi_color_num_frame = 0
        self.frame_number_counting_color = 4

        self.detect()
    

    def update_object(self,object,object_id):
        success, box = object.tracker.update(self.frame)

        if success:
            centroid = _centroid(box)
            centroid_point = Point(centroid[0], centroid[1])
            if self.region.contains(centroid_point):
                object.maxTrackingFail = 0
                object.update(box)
                '''
                Track whether the object passes or not
                '''
                self.count(object)

            else:
                object.maxTrackingFail += 1
        else:
            object.maxDetectionFail += 1
        
        if object.maxTrackingFail >= self.maxTrackingFail:
            del self.objects[object_id]
        
        if object.counted and self.object_range and not (self.object_range_poly.contains(object.centroid_point)):
            del self.objects[object_id]

    def detect(self):
        # [0,1,2,3,4] -> [with mask, no mask, incorrect mask, person, person-like]
        self.objects = add_new_objects(self.bounding_boxes, self.classes, self.confidences, self.objects, self.frame, self.maxDetectionFail, self.dupConfidenceThreshold)
        self.frame_count = 0

    
    
    def track_and_detect(self, frame, _bounding_box, _classes, _confidences):
        self.bounding_boxes = _bounding_box
        self.classes = _classes
        self.confidences = _confidences
        _timer  = cv2.getTickCount()
        self.frame = frame

    
        for _id, object in list(self.objects.items()):
            self.update_object(object, _id)

            if len(self.confidences) > 0:
                if 0 in self.confidences:
                    object.mask_on = True
                if 1 in self.confidences:
                    object.mask_off = True
                if 2 in self.confidences:
                    object.mask_incorrect = True


        if self.frame_count >= self.detection_interval:
            self.detect()
        
        self.frame_count += 1
        self.frame_rate_processing = round(cv2.getTickFrequency() / (cv2.getTickCount() - _timer), 2)
            
            

    def count(self, object):
        counted = False
        if self.counting_line:
            if (self.counting_line and not object.counted and (_pass(_type='line',l_point = object.centroid, c_line = self.counting_line, o_line = self.line_orientation) ^
                _pass(_type='line',l_point = object.position_first_detected, c_line = self.counting_line, o_line = self.line_orientation))):
                object.counted = True
                counted = True
                if not _pass(_type = 'line', l_point = object.position_first_detected, c_line = self.counting_line, o_line = self.line_orientation):
                    if object.mask_on = True:
                        self.mask_on_enter = 1
                    elif object.mask_off = True:
                        self.mask_off_enter = 1
                    else:
                        self.mask_off_enter = 1
                    self.person_in += 1
                else:
                    if object.mask_on = True:
                        self.mask_on_leave = 1
                    elif object.mask_off = True:
                        self.mask_off_leave = 1
                    else:
                        self.mask_off_leave = 1
                    self.person_out += 1
                
                self.time_end = time.time()
                self.time_send += (self.time_end - self.time_start) / 3600
                #send_requests({"mask_on_enter":self.mask_on_enter,"mask_on_leave":self.mask_on_leave,"mask_off_enter":self.mask_off_enter"mask_off_leave":self.mask_off_leave,"time":self.time_send})
            
            return counted
        
        elif self.counting_poly:

            if not object.counted and (self.counting_poly.contains(object.centroid_point) ^ self.counting_poly.contains(object.point_first_detected)):
                object.counted = True
                counted = True
                if _pass(_type='polygon', c_point = object.centroid_point, f_point=object.point_first_detected, r_polygon=self.counting_poly, o_polygon= self.counting_region_out, _enter=True):
                    if object.mask_on == True:
                        self.mask_on_enter = 1
                    elif object.mask_off == True:
                        self.mask_off_enter = 1
                    else:
                        self.mask_off_enter = 1
                    self.person_in += 1
                else:
                    if object.mask_on == True:
                        self.mask_on_leave = 1
                    elif object.mask_off == True:
                        self.mask_off_leave = 1
                    else:
                        self.mask_off_leave = 1
                    self.person_out += 1

                self.time_end = time.time()
                self.time_send += (self.time_end - self.time_start) / 3600
                #send_requests({"mask_on_enter":self.mask_on_enter,"mask_on_leave":self.mask_on_leave,"mask_off_enter":self.mask_off_enter"mask_off_leave":self.mask_off_leave,"time":self.time_send})
                print(self.mask_on_enter,self.mask_on_leave,self.mask_off_enter,self.mask_off_leave,self.time_send)

            return counted
    
    def show_result(self):
        blue = (255, 0, 0)
        yellow = (0, 255, 255)
        green = (0, 255, 0)
        orange = (0, 50, 252)
        frame = self.frame
        color = blue
        counting_roi_color = yellow

        # draw and label object bounding boxes
        for _id, object in self.objects.items():
            (x, y, w, h) = [int(v) for v in object.bounding_box]
            # blue color to the box
            color = blue
            if object.counted and not object.just_counted:
                color = green
                counting_roi_color = green
                object.object_color_num_frame = self.frame_number_counting_color
                self.roi_color_num_frame = self.frame_number_counting_color
                object.just_counted = True
            elif object.object_color_num_frame > 0:
                color = green
                object.object_color_num_frame -= 1

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            people_label = 'ID: ' + _id[:8] \
                            if object.type == None \
                            else 'ID: {0}, {1} ({2}%)'.format(_id[:8], object.type, str(object.type_confidence*100)[:4])
            cv2.putText(frame, people_label, (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 2, cv2.LINE_AA)

        # draw counting line
        if self.counting_line is not None and self.counting_region is None:
            cv2.line(frame, self.counting_line[0], self.counting_line[1], color, 3)

        # display people count
        types_counts_str = ', '.join([': '.join(map(str, i)) for i in self.types_counts.items()])
        types_counts_str = ' (' + types_counts_str + ')' if types_counts_str != '' else types_counts_str
        cv2.putText(frame, 'Count in: ' + str(self.person_in) + types_counts_str, (20, 60), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Count out: ' + str(self.person_out) + types_counts_str, (20, 120), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Processing speed: ' + str(self.frame_rate_processing) + ' FPS', (20, 180), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)

        if self.show_counting:
            if self.roi_color_num_frame > 0:
                counting_roi_color = green
                self.roi_color_num_frame -= 1
            frame = draw_roi(frame, self.counting_region, counting_roi_color)

        if self.show_object_range and self.object_range:
            frame = draw_roi(frame, self.object_range, blue)
        
        return frame

        















