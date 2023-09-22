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
#from match import Match
import asone.utils as utils
from detect import Detect
import copy
from output import Output
from threadingflask import MyThread
from flaskapp import TimeSet
class ObjectDetection:

    def __init__(self, capture_index1, capture_index2):
        self.capture_index1 = capture_index1
        self.capture_index2 = capture_index2
        self.time = TimeSet.time
        self.magnifier = 100
        self.bias = 5
        # self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # print("Using Device: ", self.device)
        self.model1 = self.load_model1()
        self.model2 = self.load_model2()
        self.CLASS_NAMES_DICT1 = self.model1.model.names
        self.CLASS_NAMES_DICT2 = self.model2.model.names
        print("Class ID1:", self.CLASS_NAMES_DICT1)
        print("Class ID2:", self.CLASS_NAMES_DICT2)
        thread1 = MyThread(1, "Thread-1")
        thread1.start()
        #thread1.join()
        print ("Started thread")
        # self.box_annotator = sv.BoxAnnotator(
        #     color=sv.ColorPalette.default(), thickness=1, text_thickness=1, text_scale=0.5)
        #self.match = Match()

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
        detect2 = ASOne(tracker=asone.BYTETRACK, detector=asone.YOLOV8M_PYTORCH, use_cuda=False)
        filter_classes = None # set to None to track all classes
        die1 = Detect()
        die2 = Detect()
        output1 = Output(1)
        output2 = Output(2)
        cam1 = "Camera1"
        cam2 = "Camera2"
        cv2.namedWindow(cam1)
        cv2.namedWindow(cam2)
        track1 = detect1.track_video(self.capture_index1, output_dir='runs/detect1', save_result=True, 
                                   display=True, filter_classes=filter_classes, 
                                   draw_trails = False, class_names = self.CLASS_NAMES_DICT1)
        track2 = detect2.track_video(self.capture_index2, output_dir='runs/detect2', save_result=True, 
                                   display=True, filter_classes=filter_classes, 
                                   draw_trails = False, class_names = self.CLASS_NAMES_DICT1)
        a = 0
        for bbox_details1, frame_details1 in track1:
            self.time = TimeSet.time
            bbox_xyxy1, ids1, scores1, class_ids1 = bbox_details1
            frame1, frame_num1, fps1, width1, height1, save_path1 = frame_details1
            bbox_details2, frame_details2 = next(track2)
            bbox_xyxy2, ids2, scores2, class_ids2 = bbox_details2
            frame2, frame_num2, fps2, width2, height2, save_path2 = frame_details2
            cleanframe1 = copy.deepcopy(frame1)
            cleanframe2 = copy.deepcopy(frame2)
            frame1 = utils.draw_boxes(frame1,
                                bbox_xyxy1,
                                class_ids1,
                                identities=ids1,
                                draw_trails=False,
                                class_names=self.CLASS_NAMES_DICT1)
            frame2 = utils.draw_boxes(frame2,
                                bbox_xyxy2,
                                class_ids2,
                                identities=ids2,
                                draw_trails=False,
                                class_names=self.CLASS_NAMES_DICT1)
            cv2.line(frame1, (140,int(height1-((height1/20)*5.3))), (360,int(height1-((height1/20)*5.3))), (255, 255, 255), 4)
            cv2.putText(frame1, f'Detail', (160, int(height1-((height1/20)*5.5))),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
            cv2.putText(frame1, f'Total: {int(len(ids1)+len(ids2))}', (60, int(height1-((height1/20)))),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            
            cv2.line(frame2, (140,int(height2-((height2/20)*5.3))), (360,int(height2-((height2/20)*5.3))), (255, 255, 255), 4)
            cv2.putText(frame2, f'Detail', (160, int(height2-(height2/20)*5.5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
            cv2.putText(frame2, f'Total: {int(len(ids1)+len(ids2))}', (60, int(height2-(height2/20))),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            cv2.imshow(cam1, frame1)          
            cv2.imshow(cam2, frame2)
            if a == 0:
                videowriter1 = cv2.VideoWriter(
                    save_path1,
                    cv2.VideoWriter_fourcc(*"avc1"),
                    1.0,
                    (int(width1), int(height1)))
                videowriter2 = cv2.VideoWriter(
                    save_path2,
                    cv2.VideoWriter_fourcc(*"avc1"),
                    1.0,
                    (int(width2), int(height2)))

            videowriter1.write(frame1)
            videowriter2.write(frame2)
            output1.print_time()
            output2.print_time()
            dead1 = die1.detecting(bbox_xyxy1, self.time, self.bias)
            dead2 = die2.detecting(bbox_xyxy2, self.time, self.bias)
            framehig1, framewid1, _ = frame1.shape
            framehig2, framewid2, _ = frame2.shape
            if dead1 != []:
                for i in range(len(dead1)):
                    for j in range(len(bbox_xyxy1)):
                        if die1.bias(bbox_xyxy1[j],dead1[i]["xyxy"]):
                            cleanframe1 = utils.draw_boxes(cleanframe1,
                                [bbox_xyxy1[j]],
                                [class_ids1[j]],
                                identities=[ids1[j]],
                                draw_trails=False,
                                class_names=self.CLASS_NAMES_DICT1)
                            crop_image1 = Detect.bboxcrop(cleanframe1,bbox_xyxy1[j],framewid1,framehig1,self.magnifier)
                            output1.store_list(cleanframe1,crop_image1,ids1[j]) 

            if dead2 != []:
                for i in range(len(dead2)):
                    for j in range(len(bbox_xyxy2)):
                        if die2.bias(bbox_xyxy2[j],dead2[i]["xyxy"]):
                            cleanframe2 = utils.draw_boxes(cleanframe2,
                                [bbox_xyxy2[j]],
                                [class_ids2[j]],
                                identities=[ids2[j]],
                                draw_trails=False,
                                class_names=self.CLASS_NAMES_DICT1)
                            crop_image2 = Detect.bboxcrop(cleanframe2,bbox_xyxy2[j],framewid2,framehig2,self.magnifier)
                            output2.store_list(cleanframe2,crop_image2,ids2[j])
            a = a + 1

        cv2.destroyWindow(cam1)
        cv2.destroyWindow(cam2)

if __name__ == '__main__':
    detector = ObjectDetection("./assets/cam1_demo3.mp4","./assets/cam1_demo3.mp4")
    detector()

# detector = ObjectDetection(0,0)
# detector()

#capture data from CCTV
# rstp_url = ['rtsp://admin:pp123123@192.168.8.47:554/Streaming/channels/201',
#             'rtsp://admin:pp123123@192.168.8.47:554/Streaming/channels/101', 'http://admin:pp123123@192.168.8.38/Streaming/channels/102/httppreview']

# detector = ObjectDetection(rstp_url[1],rstp_url[0])
# detector()
