import torch
from typing import Any
import numpy as np
import cv2
import time
from ultralytics import YOLO
import supervision as sv
import sys
import asone
from asone import ASOne

class ObjectDetection:

    def __init__(self, capture_index1, capture_index2):
        self.capture_index1 = capture_index1
        self.capture_index2 = capture_index2
        # self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # print("Using Device: ", self.device)
        self.model1 = self.load_model1()
        self.model2 = self.load_model2()
        self.CLASS_NAMES_DICT1 = self.model1.model.names
        self.CLASS_NAMES_DICT2 = self.model2.model.names
        print("Class ID1:", self.CLASS_NAMES_DICT1)
        print("Class ID2:", self.CLASS_NAMES_DICT2)
        # self.box_annotator = sv.BoxAnnotator(
        #     color=sv.ColorPalette.default(), thickness=1, text_thickness=1, text_scale=0.5)

    def load_model1(self):        
        model = YOLO("./assets/best.pt")
        model.fuse()
        return model
    
    def load_model2(self):        
        model = YOLO("./assets/best.pt")
        model.fuse()
        return model

    def __call__(self):
        # Instantiate Asone object
        detect1 = ASOne(tracker=asone.BYTETRACK, detector=asone.YOLOV8L_PYTORCH, use_cuda=False) #set use_cuda=False to use cpu
        detect2 = ASOne(tracker=asone.BYTETRACK, detector=asone.YOLOV8L_PYTORCH, use_cuda=False)
        filter_classes = None # set to None to track all classes

        # ##############################################
        #           To track using video file
        # ##############################################
        # Get tracking function
        track1 = detect1.track_stream(self.capture_index1, output_dir='runs/detect1', save_result=True, 
                                   display=True, filter_classes=filter_classes, 
                                   draw_trails = False, class_names = self.CLASS_NAMES_DICT1)
        print("finished 1, ",track1)
        track2 = detect2.track_stream(self.capture_index2, output_dir='runs/detect2', save_result=True, 
                                   display=False, filter_classes=filter_classes, 
                                   draw_trails = False, class_names = self.CLASS_NAMES_DICT2)
        print("finished 2, ",track2)
        #bbox_details2, frame_details2 = track2
        # Loop over track to retrieve outputs of each frame 
        print("going")
        for bbox_details1, frame_details1 in track1:
            print("start for loop")
            bbox_xyxy1, ids1, scores1, class_ids1 = bbox_details1
            frame1, frame_num1, fps1 = frame_details1
            print("finished call track1 data, frame1 = ", frame1)
            bbox_details2, frame_details2 = next(track2)
            bbox_xyxy2, ids2, scores2, class_ids2 = bbox_details2
            frame2, frame_num2, fps2 = frame_details2
            nMale = 0
            nFemale = 0
            for i in range(len(class_ids2)):
                if (class_ids2[i]==0):
                    nMale = nMale + 1
                else:
                    nFemale = nFemale + 1
            cv2.putText(frame1, f'Total: {int(len(class_ids1))}', (60, 800),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(frame1, f'Male: {int(nMale)}', (60, 900),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(frame1, f'Female: {int(nFemale)}', (60, 1000),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            #if display:
            cv2.imshow(' Sample', frame1)
            
            print("finished call track2 data")
            
            # Do anything with bboxes here
            print("ids = ",ids1)
            print("scores = ",scores1)
            print("class_ids = ",class_ids1)
            print("frame = ",frame1)
            print("frame_num = ",frame_num1)
            print("fps = ",fps1)

detector = ObjectDetection("./assets/demo_1.mp4","./assets/demo_2.mp4")
detector()

# detector = ObjectDetection(0,0)
# detector()

#capture data from CCTV
# rstp_url = ['rtsp://admin:pp123123@192.168.8.38:554/Streaming/channels/401',
#             'rtsp://admin:pp123123@192.168.8.38:554/Streaming/channels/201', 'http://admin:pp123123@192.168.8.38/Streaming/channels/102/httppreview']

# if __name__ == "__main__":
#     cctvNum = int(sys.argv[1])
#     if cctvNum == None or cctvNum > len(rstp_url) or cctvNum < 0:

#         quit()

#     detector = ObjectDetection(rstp_url[0],rstp_url[1])
#     detector()