import cv2
from get_pixel_coords import BoundingBoxFinder, TakeScreenshot
from setup import parser


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
    

    
    key = cv2.waitKey(1)
    # Close program with keyboard 'q'
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit(1)


    
print(finder.x)
print(finder.y)
print(finder.w)
print(finder.h)

