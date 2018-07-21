from PIL import Image
from PIL import ImageTk
import cv2
import numpy as np
import threading
from datetime import datetime

class MotionRecorder(object):

    hist_threshold = 5000    # motion sensitivity => higher the value lesser the sensitivity
    path = 0
    
    cap = cv2.VideoCapture(path)
    subtractor = cv2.createBackgroundSubtractorMOG2()
    # FourCC is a 4-byte code used to specify the video codec. The list of available codes can be found in fourcc.org.
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')     # for windows
    fps = 12
    img_counter = 0
    skip_counter = 0
    temp_img_for_video = []
    skip_first_few_frames = 0

    def __init__(self):
        pass

    def start_storing_img(self, img):
        blur = cv2.GaussianBlur(img, (19,19), 0)
        mask = self.subtractor.apply(blur)
        img_temp = np.ones(img.shape, dtype="uint8") * 255
        img_temp_and = cv2.bitwise_and(img_temp, img_temp, mask=mask)
        img_temp_and_bgr = cv2.cvtColor(img_temp_and, cv2.COLOR_BGR2GRAY)

        hist, bins = np.histogram(img_temp_and_bgr.ravel(), 256, [0,256])
        print(hist[255])

        if(self.skip_first_few_frames < 5) : 
            self.skip_first_few_frames += 1
        else : 
            if hist[255] > self.hist_threshold :
                self.skip_counter = 0
                self.img_counter += 1 
                self.temp_img_for_video.append(img)
            else : 
                self.skip_counter += 1
                if self.skip_counter >= 5 :
                    self.save_recording()

    def save_recording(self):
        if self.img_counter >= 1:   
            now = datetime.now()
            video_name = str(now.year) + str(format(now.month,'02d')) + str(format(now.day,'02d')) + str(format(now.hour,'02d')) + str(format(now.minute,'02d')) + str(format(now.second,'02d')) + ".avi"  
            out = cv2.VideoWriter("./"+video_name, self.fourcc, self.fps, (640,480))
            print(video_name)

            for image in self.temp_img_for_video : 
                out.write(image)

            self.temp_img_for_video.clear()
            self.img_counter = 0


    def start(self):
        while True :
            available, frame = self.cap.read()
            if available :
                self.start_storing_img(frame)
                cv2.imshow("Motion Recorder",frame)
                if cv2.waitKey(1) == 13 : 
                    break

    def end(self):
        self.save_recording()
        self.cap.release()
        cv2.destroyAllWindows()

MR = MotionRecorder()
MR.start()
MR.end()