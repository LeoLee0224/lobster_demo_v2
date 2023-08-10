import time

class Output:
    def __init__(self,camera_number) -> None:
        self.out_list = []
        self.cam_num = camera_number
        path = "output_log"+str(camera_number)+".txt"
        self.tfile = open(path,"w")

    def store_list(self, full_img, clo_img, track_id):

        alert = {
            "full_img": full_img,
            "clo_img": clo_img,
            "track_id": track_id,
            "cam_id": self.cam_num,
            "time": time.time()
        }
        self.out_list.append(alert)
        print("------",file=self.tfile)
        print("------",file=self.tfile)
        for item in self.out_list:
            print(str(item["track_id"]),str(item["cam_id"]),file=self.tfile)
    
    def close_log(self):
        self.tfile.close()
