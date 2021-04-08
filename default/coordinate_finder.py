import cv2
from .get_pixel_coords import BoundingBoxFinder, TakeScreenshot
from setup import parser

def get_box():

    '''
    first take a screenshot
    '''
    args = parser()
    cap = cv2.VideoCapture(args['VIDEO'])
    _, frame = cap.read()

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
        finder.show_points()

    
        key = cv2.waitKey(1)
        # Close program with keyboard 'q'
        '''
        Upon exiting get the coordinates of the last bounding box
        '''
        if key == ord('q'):
            return finder.x, finder.y, finder.w, finder.h
            cv2.destroyAllWindows()
            exit(1)



