import numpy as np
import statistics as stat
# Assume that detections_a and detections_b are lists of dictionaries, where each dictionary represents a single detection
# and has the following keys:
# - 'bbox': a tuple of (xmin, ymin, xmax, ymax) representing the bounding box coordinates
# - 'class': a string representing the class label (e.g., 'lobster', 'male', 'female')
# - 'score': a float representing the confidence score for the detection (e.g., between 0 and 1)
# - 'frame': an integer representing the frame number
# - 'id': an integer representing the ID number of the lobster

class Match:
    def __init__(self):
        self.detections_a = []
        self.detections_b = []
        self.lobster_detections = {}
        self.matched_detections = []
        self.tempclass = {}
        self.usedTrack = []
        self.waitclass = []

    def add_detection_a(self,array_bbox, array_class_id, array_score, frame, array_id):
        self.detections_a.clear()
        for i in range(len(array_id)):
            detections = {
                "bbox": array_bbox[i],
                "class": array_class_id[i],
                "score": array_score[i],
                "frame": frame,
                "id": array_id[i]
            }
            self.detections_a.append(detections)
        print("detection_A = ", self.detections_a)

    def add_detection_b(self,array_bbox, array_class_id, array_score, frame, array_id):
        self.detections_b.clear()
        for i in range(len(array_id)):
            detections = {
                "bbox": array_bbox[i],
                "class": array_class_id[i],
                "score": array_score[i],
                "frame": frame,
                "id": array_id[i]
            }
            self.detections_b.append(detections)
        print("detection_B = ", self.detections_b)

    def add_lobster_detections(self,id_a ,key,value):
        lobster_dict = {
            "number_detection": None,
            "sex_detection": None,
            "waitCount": 0
        }
        if key in lobster_dict:
            if str(id_a) in self.lobster_detections:
                if self.lobster_detections[str(id_a)]["sex_detection"] == None:
                    self.lobster_detections[str(id_a)][key] = value
                    print("in detection but not have sex,", key)
                else:
                    print("in detection but already have sex")
            else:
                lobster_dict[key] = value
                self.lobster_detections[str(id_a)] = lobster_dict
                print("not in detection,", key)
        
    def dictToList(self,lobsterDict):
        classList = []
        idsList = []
        scoreList = []
        for value in lobsterDict.values():
            if value["sex_detection"] != None:
                classList.append(value["sex_detection"])
                idsList.append(value["number_detection"]["id"])
                scoreList.append(value["number_detection"]["score"])
        return classList,idsList,scoreList


    # Define a function to match detections from Model A and Model B
    def match_detections(self):
        # Initialize a dictionary to store the detections for each lobster
        # Loop over the detections from Model A
        # Add the detection to the dictionary for the corresponding lobster
        for i in range(len(self.detections_a)):
            lobster_id = self.detections_a[i]['id']
            self.add_lobster_detections(lobster_id,"number_detection",self.detections_a[i])
        # Loop over the detections from Model B
        # Add the detection to the dictionary for the corresponding lobster
        if len(self.detections_b)==1:
            i = 0
            lobster_id = self.detections_b[i]['id']
            for key, value in self.lobster_detections.items():
                if value["sex_detection"] == None and lobster_id not in self.usedTrack:
                    if value["waitCount"]<=3:
                        self.add_lobster_detections(key,"waitCount",value["waitCount"]+1)
                        self.waitclass.append(self.detections_b[i]['class'])
                        break
                    else:
                        self.add_lobster_detections(key,"sex_detection",stat.mode(self.waitclass))
                        self.waitclass.clear()
                        print("add lobster detection and change the sex detection")
                        self.usedTrack.append(lobster_id)
                        print("used Track", self.usedTrack)
                        value["number_detection"]["score"] = float(self.detections_b[i]["score"])
                        break
        return self.lobster_detections
    
    def changeclass(self,array_ids,array_class_ids):
        finalclass = []
        # input is two arraies
        for i in range(len(array_ids)):
            ids = array_ids[i]
            class_ids = array_class_ids[i]
            if (str(ids) not in self.tempclass):
                self.tempclass[str(ids)] = []
                self.tempclass[str(ids)].append(class_ids)
                print("start record tempclass",str(ids))
            else:
                print("append tempclass")
                self.tempclass[str(ids)].append(class_ids)

            if (len(self.tempclass[str(ids)])<3):
                finalclass.append(self.tempclass[str(ids)][0])
            else:
                if (len(self.tempclass[str(ids)])>5):
                    self.tempclass[str(ids)].pop(0)
                mode = stat.mode(self.tempclass[str(ids)])
                finalclass.append(mode)

        print("self.finalclass before return is ",str(finalclass))
        return finalclass
        
