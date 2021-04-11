import cv2
from .get_pixel_coords import BoundingBoxFinder, TakeScreenshot
from .setup import parser

def get_box():

    '''
    first take a screenshot
    '''
    args = parser()
    cap_ = cv2.VideoCapture(args['VIDEO'])
    #ret, frame = cap_.read()
    
    while(True):
        ret, frame = cap_.read()
        #If frame could not be grabbed, end of feed.
        if not ret:
            print("END")
            break

        #Display output in a new window
        cv2.imshow('Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap_.release()
    cv2.destroyAllWindows
    

    '''
    W = None
    H = None


    cv2.imwrite('TestImage',frame)
    TakeScreenshot(frame,'TestImage')

    
    Get bounding box/pixel positions
    
    filepath = 'images/TestImage.jpg'
    finder = BoundingBoxFinder(filepath)

    while True:
        img = finder.show_image()
        cv2.imshow('Reference Image', img)

    
        
        # Close program with keyboard 'q'
        
        Upon exiting get the coordinates of the last bounding box
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    
    cap_.release()
    cv2.destroyAllWindows()
    return finder.x, finder.y, finder.w, finder.h


    '''
        
def get_line(orientation):

    '''
    first take a screenshot
    '''
    args = parser()
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



