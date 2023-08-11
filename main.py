from objectdetection import ObjectDetection
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from app import sever
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print ("Start thread:" + self.name)
        if self.threadID == 1:
            flask = sever()
            flask.run()
        else:
            detector = ObjectDetection("./assets/cam1_demo3.mp4","./assets/cam1_demo3.mp4")
            detector()
        print ("END thread" + self.name)


        cv2.destroyWindow(cam1)
        cv2.destroyWindow(cam2)


# detector = ObjectDetection("./assets/cam1_demo3.mp4","./assets/cam2_demo3.mp4")
# detector()

# detector = ObjectDetection(0,0)
# detector()

#capture data from CCTV
rstp_url = ['rtsp://admin:pp123123@192.168.8.47:554/Streaming/channels/201',
            'rtsp://admin:pp123123@192.168.8.47:554/Streaming/channels/101', 'http://admin:pp123123@192.168.8.38/Streaming/channels/102/httppreview']

detector = ObjectDetection(rstp_url[1],rstp_url[0])
detector()