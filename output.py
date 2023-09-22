import time
from flaskapp import TimeSet

class Output:
    def __init__(self,camera_number) -> None:
        self.cam_num = camera_number
        path = "output_log"+str(camera_number)+".txt"
        self.tfile = open(path,"w")
        self.close_log()

    def open_log(self):
        path = "output_log"+str(self.cam_num)+".txt"
        self.tfile = open(path,"a")
        
    def store_list(self, full_img, clo_img, track_id):
        alert = {
            "full_img": full_img,
            "clo_img": clo_img,
            "track_id": track_id,
            "cam_id": self.cam_num,
            "time": time.time()
        }
        self.print_list(alert)
        #send

    def print_list(self, alert):
        self.open_log()
        print("------",file=self.tfile)
        print(str(alert["track_id"]),str(alert["cam_id"]),file=self.tfile)
        print("------",file=self.tfile)
        self.close_log()
        
    def print_time(self):
        self.open_log()
        print("-------",file=self.tfile)
        print("Now setting time is ",TimeSet.time, file=self.tfile)
        print("-------",file=self.tfile)
        self.close_log()
    
    def close_log(self):
        self.tfile.close()
