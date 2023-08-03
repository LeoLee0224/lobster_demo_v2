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

    xyxy_list = []
    same = []
    time = None
    bias_level = None
    return_list = []

    def __init__(self):
        pass

    @classmethod
    def detecting(cls, array_xyxy,time_set, bias_level_set):
        cls.return_list = []
        cls.time = time_set
        cls.bias_level = bias_level_set
        if cls.xyxy_list == []:
            cls.xyxy_list = array_xyxy
        else:
            for xyxy1 in cls.xyxy_list:
                for xyxy2 in array_xyxy:
                    if cls.bias(xyxy1, xyxy2):
                        cls.add_list(xyxy2)
            cls.xyxy_list = array_xyxy
        return cls.return_list
                        
    @classmethod
    def bias(cls, xyxy1, xyxy2):
        #len(xyxy) == 4, the coordinate of left-top and the coordinate of right-bottom
        if cls.coordinate_bias(xyxy1[0],xyxy2[0]):
            if cls.coordinate_bias(xyxy1[1],xyxy2[1]):
                if cls.coordinate_bias(xyxy1[2],xyxy2[2]):
                    if cls.coordinate_bias(xyxy1[3],xyxy2[3]):
                        return True # that means the xyxy of 1 and 2 is same
        return False

    @classmethod
    def coordinate_bias(cls, int1, int2):
        if (int1+cls.bias_level>int2) and (int1-cls.bias_level<int2):
            return True
        return False
    
    @classmethod
    def add_list(cls, target):
        diction = {
            "xyxy": target,
            "time": 0
        }
        if cls.same == []:
            cls.same.append(diction)
        else:
            pop_list = []
            matched = False
            for i in range(len(cls.same)):
                if cls.bias(cls.same[i]["xyxy"],target):
                    matched = True
                    cls.same[i]["xyxy"] = target
                    cls.same[i]["time"] += 1
                    if cls.same[i]["time"] == cls.time:
                        pop_list.append(i)
            if pop_list != []:
                for i in pop_list:
                    cls.return_list.append(cls.same.pop(i))
            if matched == False:
                cls.same.append(diction)

    @staticmethod
    def bboxcrop(frame,bbox_xyxy,framewid,framehig,magnifier):
        endpoint_y = int(bbox_xyxy[3]+magnifier)
        endpoint_x = int(bbox_xyxy[2]+magnifier)
        startpoint_y = int(bbox_xyxy[1]-magnifier)
        startpoint_x = int(bbox_xyxy[0]-magnifier)
        print("range1",range(startpoint_y,endpoint_y))
        print("range2",range(startpoint_x,endpoint_x))
        wid = endpoint_x - startpoint_x
        hig = endpoint_y - startpoint_y
        if  startpoint_x < 0:
            startpoint_x = 0
            endpoint_x = endpoint_x - startpoint_x
        if  startpoint_y < 0:
            startpoint_y = 0
            endpoint_y = endpoint_y - startpoint_y
        print("framewid1 = ",framewid, "framehig1 = ", framehig)
        if  endpoint_x > framewid:
            endpoint_x = framewid
            startpoint_x = startpoint_x - (endpoint_x - framewid)
        if  endpoint_y > framehig:
            endpoint_y = framehig
            startpoint_y = startpoint_y - (endpoint_y - framehig)
            
        crop_image = frame[startpoint_y:endpoint_y, startpoint_x:endpoint_x,:]
        print("frameshape = ",frame.shape)
        print("hig = ", hig, "wid = ", wid)
        print("cropshape = ",crop_image.shape)
        print("cropimage = ", crop_image)
        return crop_image


