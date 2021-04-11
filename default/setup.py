import os
import argparse


#Using an MIPI CSI Camera needs opencv version that supports it otherwise the camera will not be
# recognized using a gstreamper pipeline. ERROR -> Camera not detected 
def gstreamer_pipeline(
    
    #BETTER FPS PERFORMACE AT 416x416
    capture_width = 416,
    capture_height = 416,
    display_width = 416,
    display_height = 416,
    framerate = 21,
    flip_method = 1 #Flip the live-feed
):
    return (
        "nvarguscamerasrc wbmode=9 ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def parser():

    webcam = gstreamer_pipeline(flip_method=2)

    arg = argparse.ArgumentParser(description="Counting the entry and exit of people")
    arg.add_argument("--YOLO",default="/darknet/",help="Directory to YOLO/Darknet")
    arg.add_argument("--PATH_WEIGHTS",default="/darknet/backup/custom_tinyYOLOv4_final.weights")
    arg.add_argument("--PATH_CFG",default="/darknet/custom_tinyYOLOv4.cfg")
    arg.add_argument("--PATH_NAMES",default="/darknet/custom_data/obj.names")
    arg.add_argument("--THRESHOLD",type=float,default=0.3,help="Minimum threshold for mask detection")
    arg.add_argument("--CONFIDENCE",type=float,default=0.3,help="Minimum probability to filter weak detections")
    arg.add_argument("--SKIP-FRAMES",type=int, default = 30, help = "Number of frames to skip in detection")
    arg.add_argument("-s", "--skip-frames", type=int, default=30,help="# of skip frames between detections")
    arg.add_argument("--VIDEO", default="/tracking-only/test.mp4",help="Video path")

    args = vars(arg.parse_args())
    args['VIDEO'] = webcam
    return args

