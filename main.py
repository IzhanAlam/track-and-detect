
import numpy as np
import os
import cv2
import imutils
from imutils.video import VideoStream
from imutils.video import FPS

from default.setup import parser
from default.setup import gstreamer_pipeline
from util.TrackAndDetect import Frame

def main():
    args = parser()

    path_label = os.path.sep.join([args["YOLO"], "custom_data/obj.names"])
    LABELS = open(path_label).read().strip().split("\n")

    #Colors to repersent each possible class (mask on, mask off, mask incorrect, person, person-like)
    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

    #Path for YOLO weights, and model
    path_weight = os.path.sep.join([args["YOLO"], "backup/custom_tinyYOLOv4_final.weights"])
    path_config = os.path.sep.join([args["YOLO"], "custom_tinyYOLOv4.cfg"])

    #Load YOLO trained on mask dataset
    print("Loading YOLO...")
    net = cv2.dnn.readNetFromDarknet(path_config,path_weight)
    #Use CUDA GPU
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    #Output layer names
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    W = None
    H = None

    cap = cv2.VideoCapture(args["VIDEO"])
    ret, frame = cap.read()
    f_height, f_width, _ = frame.shape

    detection_slowdown = True
    detection_interval = 3
    mcdf = 30

    #detector = 'csrt'

    use_droi = False
    droi = [(0, 0), (f_width, 0), (f_width, f_height), (0, f_height)]
    show_droi = False
    confidence_threshold = 0.1
    sensitive_confidence_threshold = 0.05

    mctf = 30
    tracker = "csrt"

    duplicate_object_threshold = 0.1

    use_counting_roi = False
    # [()-left up point ,()- left down point,()- right down point,()- right up point,()]
    counting_roi = [(0,380), (0,416),(416,416),(416,380)]
    show_roi_counting = True
    counting_roi_outside = False

    counting_line_orientation = None
    counting_line_position = None

    use_object_liveness = False
    roi_object_liveness = None
    show_object_liveness = False

    frame_number_counting_color = 4
    event_api_url = None

    #people_counter = FrameProcessor(frame, tracker, droi, show_droi, mcdf, mctf, detection_interval, counting_line_orientation, counting_line_position,show_roi_counting, counting_roi, counting_roi_outside, frame_number_counting_color,detection_slowdown, roi_object_liveness, show_object_liveness, confidence_threshold, sensitive_confidence_threshold,duplicate_object_threshold, event_api_url)
    people_counter = Frame(frame,tracker, mcdf, mctf, detection_interval, detection_slowdown, confidence_threshold, sensitive_confidence_threshold, duplicate_object_threshold, counting_line_orientation, counting_line_position, counting_roi, show_roi_counting, counting_roi_outside, roi_object_liveness, show_object_liveness)

    while(True):
        frame = cap.read()
        frame = frame[1]

        
        if frame is None:
            print("END")
            break


        frame = imutils.resize(frame, width = 416)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if W is None or H is None:
            (H, W) = frame.shape[:2]


        
        status = "Waiting"
        rects = []


        boxes = []
        confidences = []
        classIDs = []

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (W,H),swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > args["CONFIDENCE"]:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["CONFIDENCE"],args["THRESHOLD"])
        

        if len(idxs) > 0:
            for i in idxs.flatten():
                #status = "Detecting"
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 1)

        people_counter.track_and_detect(frame, boxes, confidences, classIDs)
        output_frame = people_counter.show_result()
        

        #Display output in a new window
        cv2.imshow('Video',output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows


if __name__ == '__main__':
    main()

