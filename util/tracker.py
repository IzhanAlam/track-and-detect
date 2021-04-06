import cv2

def csrt_create(bounding_box, frame):
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, tuple(bounding_box))
    return tracker
    

def get_tracker(bounding_box, frame):
    return csrt_create(bounding_box, frame)