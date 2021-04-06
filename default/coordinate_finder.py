import cv2
from .get_pixel_coordinates import BoundingBoxFinder, TakeScreenshot
from setup import parser

'''
first take a screenshot
'''
args = parser()
cap = cv2.VideoCapture(args['VIDEO'])
_, frame = cap.read()

W = None
H = None

TakeScreenshot('TestImage')

'''
Get bounding box/pixel positions
'''
filepath = 'images/TestImage.jpg'
finder = BoundingBoxFinder(filepath)

while True:
    cv2.imshow('Reference Image', BoundingBoxFinder.show_image())
    key = cv2.waitKey(1)
    # Close program with keyboard 'q'
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit(1)


    


