import cv2    

def get_tracker(bounding_box, frame):
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, tuple(bounding_box))
    return tracker