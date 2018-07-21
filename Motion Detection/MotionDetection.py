import cv2
import numpy as np
import winsound

class MotionDetection(object) : 

    #path = "../videos/walking.avi"
	path = 0
    cap = cv2.VideoCapture(path)
    sub = cv2.createBackgroundSubtractorMOG2()
    threshold = 5000
    frequency = 400
    
    def __init__(self) : 
        pass

    def start(self) : 
        while(True):
            ret, frame = self.cap.read()
    
            cv2.imshow("Motion Detection",frame)
            blur = cv2.GaussianBlur(frame,(19,19),0)
            mask = self.sub.apply(blur)
            #cv2.imshow("sub",mask)
            img_temp = np.ones(frame.shape,dtype="uint8") * 255
            img_temp_and = cv2.bitwise_and(img_temp,img_temp,mask=mask)
            img_temp_and_bgr = cv2.cvtColor(img_temp_and,cv2.COLOR_BGR2GRAY)    
            hist,bins = np.histogram(img_temp_and_bgr.ravel(),256,[0,256]) 
            print("Threshold =", self.threshold, ", Noise = ",hist[255], )

            if hist[255] > self.threshold : 
                winsound.Beep(self.frequency,100)    # winsound.Beep(frequency, duration)
                
            if cv2.waitKey(100) == 13 :
                break

    def end(self) : 
        self.cap.release()
        cv2.destroyAllWindows()

MD = MotionDetection()
MD.start()
MD.end()

