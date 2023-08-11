from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from app import sever
import threading
import time

exitFlag = 0

class MyThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print ("Start thread:" + self.name)
        if self.threadID == 1:
            flask = sever()
            flask.run()
        print ("END thread" + self.name)


# if __name__ == '__main__':
#     thread1 = MyThread(1, "Thread-1")
#     thread2 = MyThread(2, "Thread-2")
#     thread1.start()
#     thread2.start()
#     thread1.join()
#     thread2.join()
#     print ("Stop all threads")