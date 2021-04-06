
from .bbox import _centroid, _area, _overlap
from shapely.geometry import Point
from .tracker import get_tracker
import uuid

class DetectedObject:
    def __init__(self, bounding_box_, type_, confidence_, tracker_):

        self.bounding_box = bounding_box_
        self.type = type_
        self.type_confidence = confidence_

        self.centroid = _centroid(bounding_box_)
        self.centroid_point = Point(self.centroid[0], self.centroid[1])
        self.area = _area(bounding_box_)
        self.tracker = tracker_

        self.num_consecutive_tracking_failures = 0
        self.num_consecutive_detection_failures = 0

        self.counted = False
        self.just_counted = False


        self.mask_on = 0
        self.mask_off = 0
        self.mask_incorrect = 0

        self.object_color_num_frame = 0
        self.position_first_detected = tuple(self.centroid) 
        self.point_first_detected = Point(self.position_first_detected[0], self.position_first_detected[1])

    
    def update(self, bounding_box_, type_=None, confidence_=None, tracker_=None):
        self.bounding_box = bounding_box_
        self.type = type_ if type_ != None else self.type
        self.type_confidence = confidence_ if confidence_ != None else self.type_confidence
        self.centroid = _centroid(bounding_box_)
        self.centroid_point = Point(self.centroid[0], self.centroid[1])
        self.area = _area(bounding_box_)

        if tracker_:
            self.tracker = tracker_


def add_new_objects(boxes, classes, confidences, objects, frame, mcdf, overlap_threshold):

    matched_object_ids = []
    for i, box in enumerate(boxes):
        type_ = classes[i] if classes is not None else None
        confidence_ = confidences[i] if confidences is not None else None
        tracker_ = get_tracker(box, frame)

        match_found = False
        for _id, object in objects.items():
            if _overlap(box, object.bounding_box) >= overlap_threshold:
                match_found = True
                if _id not in matched_object_ids:
                    object.num_consecutive_detection_failures = 0
                    matched_object_ids.append(_id)
                object.update(box, type_, confidence_, tracker_)
                break

        if not match_found:
            # create new object
            _object = DetectedObject(box, type_, confidence_, tracker_)
            object_id = generate_people_id()
            objects[object_id] = _object

    objects = remove_object_oof(objects, matched_object_ids, mcdf)
    return remove_duplicates(objects, overlap_threshold)

def remove_object_oof(objects,matched_object_ids, mcdf):

    for _id, object in list(objects.items()):
        if _id not in matched_object_ids:
            object.num_consecutive_detection_failures += 1
        if object.num_consecutive_detection_failures > mcdf:
            del objects[_id]
    return objects

def remove_duplicates(objects, overlap_threshold):

    for _id, object_a in list(objects.items()):
        for _, object_b in list(objects.items()):
            if object_a == object_b:
                break
            overlap = _overlap(object_a.bounding_box, object_b.bounding_box)

            if overlap >= overlap_threshold and _id in objects:
                del objects[_id]
    return objects

def generate_people_id():
    return 'id_' + uuid.uuid4().hex




