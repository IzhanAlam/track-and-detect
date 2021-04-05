'''
Utility functions to calculate bounding box properties
'''
# Get centroid
def _centroid(bbox):
    x,y,w,h = bbox
    return round((x + x + w) / 2), round((y + y + h) / 2)

# Get area
def _area(bbox):
    x,y,w,h = bbox
    return w*h

# Get Overlap between two bounding boxes
def _overlap(bbox1, bbox2):
    bbox1_x1 = bbox1[0]
    bbox1_y1 = bbox1[1]
    bbox1_x2 = bbox1[0] + bbox1[2]
    bbox1_y2 = bbox1[1] + bbox1[3]

    bbox2_x1 = bbox2[0]
    bbox2_y1 = bbox2[1]
    bbox2_x2 = bbox2[0] + bbox2[2]
    bbox2_y2 = bbox2[1] + bbox2[3]

    overlap_x1 = max(bbox1_x1, bbox2_x1)
    overlap_y1 = max(bbox1_y1, bbox2_y1)
    overlap_x2 = min(bbox1_x2, bbox2_x2)
    overlap_y2 = min(bbox1_y2, bbox2_y2)

    overlap_width = overlap_x2 - overlap_x1
    overlap_height = overlap_y2 - overlap_y1

    if overlap_width < 0 or overlap_height < 0:
        return 0.0

    overlap_area = overlap_width * overlap_height

    bbox1_area = (bbox1_x2 - bbox1_x1) * (bbox1_y2 - bbox1_y1)
    bbox2_area = (bbox2_x2 - bbox2_x1) * (bbox2_y2 - bbox2_y1)
    smaller_area = bbox1_area if bbox1_area < bbox2_area else bbox2_area

    epsilon = 0.00001
    overlap = overlap_area / (smaller_area + epsilon)
    return overlap

# Get image area of bounding box
def _image(frame,bbox):
    x, y, w, h = list(map(int, bbox))
    return frame[y - 10:y + h + 10, x - 10:x + w + 10] 
