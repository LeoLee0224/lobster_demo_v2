import numpy as np
# Assume that detections_a and detections_b are lists of dictionaries, where each dictionary represents a single detection
# and has the following keys:
# - 'bbox': a tuple of (xmin, ymin, xmax, ymax) representing the bounding box coordinates
# - 'class': a string representing the class label (e.g., 'lobster', 'male', 'female')
# - 'score': a float representing the confidence score for the detection (e.g., between 0 and 1)
# - 'frame': an integer representing the frame number
# - 'id': an integer representing the ID number of the lobster

class Match:
    def __init__(self):
        self.detections_a = {}
        self.detections_b = {}
        self.lobster_detections = {}
        self.matched_detections = []
        self.tempclass = {}
        self.finalclass = None

    def add_detection_a(self,bbox,class_id,score,frame,id):
        detections = {
            "bbox": bbox,
            "class": class_id,
            "score": score,
            "frame": frame,
            "id": id
        }
        self.detections_a = detections
        print("detection_A = ", self.detections_a)

    def add_detection_b(self,bbox,class_id,score,frame,id):
        detections = {
            "bbox": bbox,
            "class": class_id,
            "score": score,
            "frame": frame,
            "id": id
        }
        self.detections_b = detections
        print("detection_B = ", self.detections_b)

    # Define a function to match detections from Model A and Model B
    def match_detections(self):
        # Initialize a dictionary to store the detections for each lobster
        # Loop over the detections from Model A
        # Add the detection to the dictionary for the corresponding lobster
        lobster_id = self.detections_a['id']
        if lobster_id not in self.lobster_detections.items():
            self.lobster_detections[str(lobster_id)] = {'number_detection': self.detections_a}
        else:
            self.lobster_detections[str(lobster_id)]['number_detection'] = self.detections_a
        # Loop over the detections from Model B
        # Add the detection to the dictionary for the corresponding lobster
        lobster_id = self.detections_b['id']
        if lobster_id in self.lobster_detections.items():
            self.lobster_detections[str(lobster_id)]['sex_detection'] = self.detections_b
        print("lobster_id = ", lobster_id)
        # Combine the matched detections for each lobster
        for lobster_id, detections in self.lobster_detections.items():
            if 'number_detection' in detections and 'sex_detection' in detections:
                matched_detection = {
                    'bbox': detections['number_detection']['bbox'],
                    'class': detections['number_detection']['class'] + ' ' + detections['sex_detection']['class'],
                    'score': (detections['number_detection']['score'] + detections['sex_detection']['score']) / 2
                }
                self.matched_detections.append(matched_detection)
        return self.matched_detections
    
    def changeclass(self,ids,class_ids):
        if (str(ids) not in self.tempclass):
            self.tempclass[str(ids)] = [class_ids]
            print("start record tempclass",str(ids))
        else:
            self.tempclass[str(ids)].append(class_ids)
        if (len(self.tempclass[str(ids)])<3):
            self.finalclass = self.tempclass[str(ids)][0]
        else:
            length = len(self.tempclass[str(ids)])
            if (self.tempclass[str(ids)][length-1]==self.tempclass[str(ids)][length-2]==self.tempclass[str(ids)][length-3]):
                self.finalclass = self.tempclass[str(ids)][length-1]
        return self.finalclass
