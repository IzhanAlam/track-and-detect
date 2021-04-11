
import numpy as np
import os
import cv2
import imutils
from imutils.video import VideoStream
from imutils.video import FPS

from default.setup import parser
from default.setup import gstreamer_pipeline
from util.TrackAndDetect import Frame
from initializer import frame_setup

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

    cap = cv2.VideoCapture(args['VIDEO'])
    cap.set(3,416)
    cap.set(4,416)
    _, frame = cap.read()
    W = None
    H = None

    counter = frame_setup(frame)
    print("STARTING...setting up detection and tracking...")
    while(True):
        frame = cap.read()
        frame = frame[1]

        
        if frame is None:
            print("END")
            break


        frame = imutils.resize(frame, height=416,width = 416)

        if W is None or H is None:
            (H, W) = frame.shape[:2]



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
        
        '''
        if len(idxs) > 0:
            for i in idxs.flatten():
                #status = "Detecting"
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
                text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                cv2.putText(frame, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 1)
        '''

        counter.track_and_detect(frame, boxes, confidences, classIDs)
        output_frame = counter.show_result()
        

        #Display output in a new window
        cv2.imshow('Video',output_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows


if __name__ == '__main__':
    main()

