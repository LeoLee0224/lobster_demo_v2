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

class Detect:

    def __init__(self):
        self.xyxy_list = []
        self.same = []
        self.time = None
        self.bias_level = None
        self.return_list = []

    def detecting(self, array_xyxy,time_set, bias_level_set):
        self.return_list = []
        self.time = time_set
        self.bias_level = bias_level_set
        if self.xyxy_list == []:
            self.xyxy_list = array_xyxy
        else:
            for xyxy1 in self.xyxy_list:
                for xyxy2 in array_xyxy:
                    if self.bias(xyxy1, xyxy2):
                        self.add_list(xyxy2)
            self.xyxy_list = array_xyxy
        return self.return_list
                        
    def bias(self, xyxy1, xyxy2):
        #len(xyxy) == 4, the coordinate of left-top and the coordinate of right-bottom
        if self.coordinate_bias(xyxy1[0],xyxy2[0]):
            if self.coordinate_bias(xyxy1[1],xyxy2[1]):
                if self.coordinate_bias(xyxy1[2],xyxy2[2]):
                    if self.coordinate_bias(xyxy1[3],xyxy2[3]):
                        return True # that means the xyxy of 1 and 2 is same
        return False

    def coordinate_bias(self, int1, int2):
        if (int1+self.bias_level>int2) and (int1-self.bias_level<int2):
            return True
        return False
    
    def add_list(self, target):
        diction = {
            "xyxy": target,
            "time": 0
        }
        if self.same == []:
            self.same.append(diction)
        else:
            matched = False
            i = 0
            leng = len(self.same)
            while i < leng:
                if self.bias(self.same[i]["xyxy"],target):
                    matched = True
                    self.same[i]["xyxy"] = target
                    self.same[i]["time"] += 1
                    if self.same[i]["time"] >= self.time:
                        self.return_list.append(self.same.pop(i))
                        i = i - 1
                        leng = leng - 1
                i = i + 1
            if matched == False:
                self.same.append(diction)

    @staticmethod
    def bboxcrop(frame,bbox_xyxy,framewid,framehig,magnifier):
        endpoint_y = int(bbox_xyxy[3]+magnifier)
        endpoint_x = int(bbox_xyxy[2]+magnifier)
        startpoint_y = int(bbox_xyxy[1]-magnifier)
        startpoint_x = int(bbox_xyxy[0]-magnifier)
        # print("range1",range(startpoint_y,endpoint_y))
        # print("range2",range(startpoint_x,endpoint_x))
        wid = endpoint_x - startpoint_x
        hig = endpoint_y - startpoint_y
        if  startpoint_x < 0:
            startpoint_x = 0
            endpoint_x = endpoint_x - startpoint_x
        if  startpoint_y < 0:
            startpoint_y = 0
            endpoint_y = endpoint_y - startpoint_y
        #print("framewid1 = ",framewid, "framehig1 = ", framehig)
        if  endpoint_x > framewid:
            endpoint_x = framewid
            startpoint_x = startpoint_x - (endpoint_x - framewid)
        if  endpoint_y > framehig:
            endpoint_y = framehig
            startpoint_y = startpoint_y - (endpoint_y - framehig)
            
        crop_image = frame[startpoint_y:endpoint_y, startpoint_x:endpoint_x,:]
        # print("frameshape = ",frame.shape)
        # print("hig = ", hig, "wid = ", wid)
        # print("cropshape = ",crop_image.shape)
        # print("cropimage = ", crop_image)
        return crop_image


