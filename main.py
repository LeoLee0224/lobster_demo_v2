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

        # ##############################################
        #           To track using video file
        # ##############################################
        # Get tracking function
        cam1 = "Camera1"
        cam2 = "Camera2"
        cv2.namedWindow(cam1)
        cv2.namedWindow(cam2)
        #self.CLASS_NAMES_DICT1 = {3:self.CLASS_NAMES_DICT1[0]}
        track1 = detect1.track_video(self.capture_index1, output_dir='runs/detect1', save_result=True, 
                                   display=True, filter_classes=filter_classes, 
                                   draw_trails = False, class_names = self.CLASS_NAMES_DICT1)
        print("finished 1, ",track1)
        track2 = detect2.track_video(self.capture_index2, output_dir='runs/detect2', save_result=True, 
                                   display=True, filter_classes=filter_classes, 
                                   draw_trails = False, class_names = self.CLASS_NAMES_DICT1)
        print("finished 2, ",track2)
        # Loop over track to retrieve outputs of each frame 
        print("going")
        a = 0
        for bbox_details1, frame_details1 in track1:
            print("start for loop")
            bbox_xyxy1, ids1, scores1, class_ids1 = bbox_details1
            frame1, frame_num1, fps1, width1, height1, save_path1 = frame_details1
            #self.match.confidenceAndEdit(bbox_xyxy1,class_ids1,scores1,ids1,0.7)
            #self.match.add_detection_a(bbox_xyxy1,class_ids1,scores1,frame_num1,ids1)
            print("finished call track1 data")
            bbox_details2, frame_details2 = next(track2)
            bbox_xyxy2, ids2, scores2, class_ids2 = bbox_details2
            frame2, frame_num2, fps2, width2, height2, save_path2 = frame_details2
            #self.match.confidenceAndEdit(bbox_xyxy2,class_ids2,scores2,ids2,0.7)
            #self.match.add_detection_b(bbox_xyxy2,class_ids2,scores2,frame_num2,ids2)
            print("finished call track2 data")
            #match_result = self.match.match_detections()
            #print("match_result = ",match_result)
            #matchClass, matchids, matchScore = self.match.dictToList(match_result)
            #matchBBox = []
            #matchOriScore = []
            # for i in range(len(class_ids1)):
            #     class_ids1[i] = class_ids1[i]+3
            # leng = len(matchids)
            # i = 0
            # while i < leng:
            #     if matchids[i] in ids1:
            #         listIndex = ids1.index(matchids[i])
            #         class_ids1.pop(listIndex)
            #         ids1.pop(listIndex)
            #         matchBBox.append(bbox_xyxy1.pop(listIndex))
            #         matchOriScore.append(scores1.pop(listIndex))
            #         print("ori pop finished")
            #     else:
            #         matchClass.pop(i)
            #         matchids.pop(i)
            #         matchScore.pop(i)
            #         i = i - 1
            #         leng = leng - 1
            #         print("match pop finished")
            #     i = i + 1
            # for i in range(len(matchScore)):
            #     matchScore[i] = (matchScore[i]+matchOriScore[i])/2
            print("write boxese")
            #print scores class_ids and ids
            frame1 = utils.draw_boxes(frame1,
                                bbox_xyxy1,
                                class_ids1,
                                identities=ids1,
                                draw_trails=False,
                                class_names=self.CLASS_NAMES_DICT1)
            # if len(matchids) != 0:
            frame2 = utils.draw_boxes(frame2,
                                bbox_xyxy2,
                                class_ids2,
                                identities=ids2,
                                draw_trails=False,
                                class_names=self.CLASS_NAMES_DICT1)
            #finalclass2 = self.match.changeclass(ids2,class_ids2)
            # finalclass2 = class_ids2
            # frame2 = utils.draw_boxes(frame2,
            #                     bbox_xyxy2,
            #                     finalclass2,
            #                     identities=ids2,
            #                     draw_trails=False,
            #                     class_names=self.CLASS_NAMES_DICT2,
            #                     score=scores2)
            # nMale = 0
            # nFemale = 0
            # nUndefine = 0
            # for i in range(len(matchClass)):
            #     if (matchClass[i]==1):
            #         nMale = nMale + 1
            #     elif(matchClass[i]==0):
            #         nFemale = nFemale + 1
            #     else:
            #         nUndefine = nUndefine + 1
            cv2.line(frame1, (140,int(height1-((height1/20)*5.3))), (360,int(height1-((height1/20)*5.3))), (255, 255, 255), 4)
            cv2.putText(frame1, f'Detail', (160, int(height1-((height1/20)*5.5))),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
            cv2.putText(frame1, f'Total: {int(len(ids1)+len(ids2))}', (60, int(height1-((height1/20)))),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            # cv2.putText(frame1, f'Male: {int(nMale)}', (60, int(height1-(height1/20)*4)),
            #         cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 100, 100), 5)
            # cv2.putText(frame1, f'Female: {int(nFemale)}', (60, int(height1-(height1/20)*3)),
            #         cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            # cv2.putText(frame1, f'Undefine: {int(nUndefine)}', (60, int(height1-(height1/20)*2)),
            #         cv2.FONT_HERSHEY_SIMPLEX, 2, (250, 112, 250), 5)
            
            cv2.line(frame2, (140,int(height2-((height2/20)*5.3))), (360,int(height2-((height2/20)*5.3))), (255, 255, 255), 4)
            cv2.putText(frame2, f'Detail', (160, int(height2-(height2/20)*5.5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
            cv2.putText(frame2, f'Total: {int(len(ids1)+len(ids2))}', (60, int(height2-(height2/20))),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
            # cv2.putText(frame2, f'Male: {int(nMale)}', (60, int(height2-(height2/20)*4)),
            #         cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 100, 100), 5)
            # cv2.putText(frame2, f'Female: {int(nFemale)}', (60, int(height2-(height2/20)*3)),
            #         cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            # cv2.putText(frame2, f'Undefine: {int(nUndefine)}', (60, int(height2-(height2/20)*2)),
            #         cv2.FONT_HERSHEY_SIMPLEX, 2, (250, 112, 250), 5)
            #if display:
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
            path = "mainlog.txt"
            tfile = open(path,"a")
            magnifier = 100
            dead1 = Detect.detecting(bbox_xyxy1, 3, 5)
            dead2 = Detect.detecting(bbox_xyxy2, 3, 5)
            framehig1, framewid1, _ = frame1.shape
            framehig2, framewid2, _ = frame2.shape
            print("framehig1 = ",framehig1, "framewid = ", framewid1)
            if dead1 != []:
                print("pop list in dead1",file=tfile)
                for i in range(len(dead1)):
                    for j in range(len(bbox_xyxy1)):
                        if Detect.bias(bbox_xyxy1[j],dead1[i]["xyxy"]):
                            print("bbox = ",bbox_xyxy1[j],"track_id = ",ids1[j],"finished printing",file=tfile)
                            crop_image1 = Detect.bboxcrop(frame1,bbox_xyxy1[j],framewid1,framehig1,magnifier)
                            img_name1 = "runs/detect3/output"+str(frame_num1)+"_"+str(i)+".jpg"
                            cv2.imwrite(img_name1,crop_image1)
                            
            if dead2 != []:
                print("pop list in dead2",file=tfile)
                for i in range(len(dead2)):
                    for j in range(len(bbox_xyxy2)):
                        if Detect.bias(bbox_xyxy2[j],dead2[i]["xyxy"]):
                            print("bbox = ",bbox_xyxy2[j],"track_id = ",ids2[j],"finished printing",file=tfile)
                            crop_image2 = Detect.bboxcrop(frame2,bbox_xyxy2[j],framewid2,framehig2,magnifier)
                            img_name2 = "runs/detect4/output"+str(frame_num2)+"_"+str(i)+".jpg"
                            cv2.imwrite(img_name2,crop_image2)

            tfile.close()
            # Do anything with bboxes here
            print("ids1 = ",ids1)
            print("scores1 = ",scores1)
            print("class_ids1 = ",class_ids1)
            print("frame_num1 = ",frame_num1)
            print("fps1 = ",fps1)
            print("ids2 = ",ids2)
            print("scores2 = ",scores2)
            print("class_ids2 = ",class_ids2)
            print("frame_num2 = ",frame_num2)
            print("fps2 = ",fps2)
            print("save_path1 = ",save_path1)
            a = a + 1

        cv2.destroyWindow(cam1)
        cv2.destroyWindow(cam2)


detector = ObjectDetection("./assets/cam1_demo3.mp4","./assets/cam1_demo3.mp4")
detector()

# detector = ObjectDetection(0,0)
# detector()

#capture data from CCTV
# rstp_url = ['rtsp://admin:pp123123@192.168.8.47:554/Streaming/channels/201',
#             'rtsp://admin:pp123123@192.168.8.47:554/Streaming/channels/101', 'http://admin:pp123123@192.168.8.38/Streaming/channels/102/httppreview']

# detector = ObjectDetection(rstp_url[1],rstp_url[0])
# detector()