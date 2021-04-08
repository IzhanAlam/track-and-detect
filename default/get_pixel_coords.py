'''
Function to help get coordinates for entry/exit pass points
'''

import cv2
import pathlib
import os
class BoundingBoxFinder:
    def __init__(self,filepath):
        self.original_image = cv2.imread(str(filepath))
        self.copy = self.original_image

        cv2.namedWindow('Reference Image')
        cv2.setMouseCallback('Reference Image', self.extract_coordinates)
        self.image_coordinates = []

    
    def extract_coordinates(self, event, x, y,flags, parameters):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]

        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            print('top left: {}, bottom right: {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
            print('x,y,w,h : ({}, {}, {}, {})'.format(self.image_coordinates[0][0], self.image_coordinates[0][1], self.image_coordinates[1][0] - self.image_coordinates[0][0], self.image_coordinates[1][1] - self.image_coordinates[0][1]))

            cv2.rectangle(self.copy, self.image_coordinates[0], self.image_coordinates[1], (36,255,12), 2)
            cv2.imshow("Reference Image", self.copy)
        
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.copy = self.original_image.copy()
    
    def show_image(self):
        #return a copy of the img, the x,y,w,h
        return self.copy, self.image_coordinates[0][0], self.image_coordinates[0][1], self.image_coordinates[1][0] - self.image_coordinates[0][0], self.image_coordinates[1][1] - self.image_coordinates[0][1]
    


def TakeScreenshot(frame,filename):
    screenshots_directory = 'images/'
    pathlib.Path(screenshots_directory).mkdir(parents=True, exist_ok=True)
    screenshot_path = os.path.join(screenshots_directory, str(filename) +  '.jpg')
    cv2.imwrite(screenshot_path,frame, [cv2.IMWRITE_JPEG_QUALITY, 80])



