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
from match import Match

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
        self.match = Match()

    def load_model1(self):        
        model = YOLO("./assets/best.pt")
        model.fuse()
        return model
    
    def load_model2(self):        
        model = YOLO("./assets/best_v2.pt")
        model.fuse()
        return model

    def __call__(self):
        # Instantiate Asone object
        detect1 = ASOne(tracker=asone.BYTETRACK, detector=asone.YOLOV8M_PYTORCH, use_cuda=False) #set use_cuda=False to use cpu
        detect2 = ASOne(tracker=asone.BYTETRACK, detector=asone.YOLOV8S_PYTORCH, use_cuda=False)
        filter_classes = None # set to None to track all classes

        # ##############################################
        #           To track using video file
        # ##############################################
        # Get tracking function
        cam1 = "Camera1"
        cam2 = "Camera2"
        cv2.namedWindow(cam1)
        cv2.namedWindow(cam2)

        track1 = detect1.track_video(self.capture_index1, output_dir='runs/detect1', save_result=True, 
                                   display=True, filter_classes=filter_classes, 
                                   draw_trails = False, class_names = self.CLASS_NAMES_DICT1)
        print("finished 1, ",track1)
        track2 = detect2.track_video(self.capture_index2, output_dir='runs/detect2', save_result=True, 
                                   display=True, filter_classes=filter_classes, 
                                   draw_trails = False, class_names = self.CLASS_NAMES_DICT2)
        print("finished 2, ",track2)
        #bbox_details2, frame_details2 = track2
        # Loop over track to retrieve outputs of each frame 
        print("going")
        for bbox_details1, frame_details1 in track1:
            print("start for loop")
            bbox_xyxy1, ids1, scores1, class_ids1 = bbox_details1
            frame1, frame_num1, fps1, width1, height1, save_path1 = frame_details1
            self.match.add_detection_a(bbox_xyxy1,class_ids1,scores1,frame_num1,ids1)
            print("finished call track1 data")
            bbox_details2, frame_details2 = next(track2)
            bbox_xyxy2, ids2, scores2, class_ids2 = bbox_details2
            frame2, frame_num2, fps2, width2, height2, save_path2 = frame_details2
            self.match.add_detection_b(bbox_xyxy2,class_ids2,scores2,frame_num2,ids2)
            print("finished call track2 data")
            match_result = self.match.match_detections()
            print("match_result = ",match_result)
            nMale = 0
            nFemale = 0
            nUndefine = 0
            for i in range(len(class_ids2)):
                if (class_ids2[i]==1):
                    nMale = nMale + 1
                elif(class_ids2[i]==0):
                    nFemale = nFemale + 1
                else:
                    nUndefine = nUndefine + 1
            cv2.putText(frame1, f'Total: {int(len(ids1))}', (60, 800),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(frame1, f'Male: {int(nMale)}', (60, 900),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(frame1, f'Female: {int(nFemale)}', (60, 1000),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(frame1, f'Undefine: {int(nUndefine)}', (60, 1200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

            cv2.putText(frame2, f'Total: {int(len(ids1))}', (60, 800),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(frame2, f'Male: {int(nMale)}', (60, 900),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(frame2, f'Female: {int(nFemale)}', (60, 1000),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            cv2.putText(frame2, f'Undefine: {int(nUndefine)}', (60, 1200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
            #if display:
            cv2.imshow(cam1, frame1)          
            cv2.imshow(cam2, frame2)          
            cv2.VideoWriter(
                save_path1,
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps1,
                (int(width1), int(height1)),
            ).write(frame1)
            cv2.VideoWriter(
                save_path2,
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps2,
                (int(width2), int(height2)),
            ).write(frame2)
            # Do anything with bboxes here
            print("ids1 = ",ids1)
            print("scores1 = ",scores1)
            print("class_ids1 = ",class_ids1)
            print("frame1 = ",frame1)
            print("frame_num1 = ",frame_num1)
            print("fps1 = ",fps1)
            print("ids2 = ",ids2)
            print("scores2 = ",scores2)
            print("class_ids2 = ",class_ids2)
            print("frame2 = ",frame2)
            print("frame_num2 = ",frame_num2)
            print("fps2 = ",fps2)

        cv2.destroyWindow(cam1)
        cv2.destroyWindow(cam2)


detector = ObjectDetection("./assets/cam1_demo3.mp4","./assets/cam2_demo3.mp4")
detector()

# detector = ObjectDetection(0,0)
# detector()

#capture data from CCTV
# rstp_url = ['rtsp://admin:pp123123@192.168.8.38:554/Streaming/channels/401',
#             'rtsp://admin:pp123123@192.168.8.38:554/Streaming/channels/201', 'http://admin:pp123123@192.168.8.38/Streaming/channels/102/httppreview']

# detector = ObjectDetection(rstp_url[1],rstp_url[0])
# detector()