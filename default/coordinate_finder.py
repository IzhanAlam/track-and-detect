import cv2
from .get_pixel_coords import BoundingBoxFinder, TakeScreenshot
from .setup import parser

import imutils
from imutils.video import VideoStream

def get_box():
    '''
    first take a screenshot
    '''
    args = parser()
    args['VIDEO'] = "/tracking-only/test.mp4"
    cap_ = cv2.VideoCapture(args['VIDEO'])
    _, frame = cap_.read()

    W = None
    H = None

    TakeScreenshot(frame,'TestImage')

    '''
    Get bounding box/pixel positions
    '''
    filepath = 'images/TestImage.jpg'
    finder = BoundingBoxFinder(filepath)

    while True:
        img = finder.show_image()
        cv2.imshow('Reference Image', img)
        
        frame = cap_.read()
        frame = frame[1]

        

        if W is None or H is None:
            (H, W) = frame.shape[:2]
        
        # Close program with keyboard 'q'
        '''
        Upon exiting get the coordinates of the last bounding box
        '''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    
    cap_.release()
    cv2.destroyAllWindows()
    
    
    cap_.release()
    cv2.destroyAllWindows()
    
    return finder.x, finder.y, finder.w, finder.h
    


    
        
def get_line(orientation):

    '''
    first take a screenshot
    '''
    args = parser()
    args['VIDEO'] = "/tracking-only/test.mp4"
    cap_ = cv2.VideoCapture(args['VIDEO'])
    _, frame = cap_.read()

    W = None
    H = None

    TakeScreenshot(frame,'TestImage')

    '''
    Get bounding box/pixel positions
    '''
    filepath = 'images/TestImage.jpg'
    finder = BoundingBoxFinder(filepath)

    while True:
        img = finder.show_image()
        cv2.imshow('Reference Image', img)
        
        frame = cap_.read()
        frame = frame[1]

        

        if W is None or H is None:
            (H, W) = frame.shape[:2]
        
        # Close program with keyboard 'q'
        '''
        Upon exiting get the coordinates of the last bounding box
        '''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    
    cap_.release()
    cv2.destroyAllWindows()
    if orientation == 'right' or orientation == 'left':
        return ((finder.x + finder.w)/W)

    elif orientation == 'bottom' or orientation == 'top':
        return ((finder.y + finder.h)/ H)



