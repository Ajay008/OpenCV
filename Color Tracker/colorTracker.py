import cv2
import numpy as np


class ColorTracker(object):
    #path = "../videos/ball.mp4"
    path = 0                        # set the path of video to load and for primary camera keep it 0, for second camera 1 and so on.
    hue_tolerance = 5
    
    mouse_clicked = False
    frame = np.zeros((480,640,3), np.uint8)
    b, g, r = 0, 0, 0
    cx, cy = 0, 0
    cap = None
    color_lower_range = (0,0,0)
    color_higher_range = (0,0,0)

    def __init__(self) :
        self.cap = cv2.VideoCapture(self.path)
        cv2.namedWindow("Color Tracker")
        cv2.setMouseCallback('Color Tracker', self.getCoords)

    def getCoords(self,event,x,y,flags,param) :
        if event == cv2.EVENT_LBUTTONDOWN:
            self.cx, self.cy = x, y
            
            self.b, self.g, self.r = self.frame[self.cy,self.cx]
            self.b, self.g, self.r = int(self.b), int(self.g), int(self.r)

            frame_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            h,s,v = frame_hsv[self.cy,self.cx]
            h,s,v = int(h),int(s),int(v)
            print(h,s,v)

            h_low = h - self.hue_tolerance
            h_high = h + self.hue_tolerance
            if h_low < 0 :
                h_low = 0
            if h_high > 179 : 
                h_high = 179
            
            s_low = s - 10
            s_high = s + 10
            if s_low < 0 :
                s_low = 0
            if s_high > 255 : 
                s_high = 255

            v_low = v - 15
            v_high = v + 15
            if v_low < 0 :
                v_low = 0
            if v_high > 255 : 
                v_high = 255
                

            self.color_lower_range = (h_low,100,100)
            self.color_higher_range = (h_high,255,255)
            
            if s < 100 :
                self.color_lower_range = (h_low,s_low,100)
                self.color_higher_range = (h_high,s_high,255)
            if v < 100 :
                self.color_lower_range = (h_low,100,v_low)
                self.color_higher_range = (h_high,255,v_high)
            if s<100 and v<100 : 
                self.color_lower_range = (h_low,s_low,v_low)
                self.color_higher_range = (h_high,s_high,v_high)

            self.mouse_clicked = True            


    def start(self) :
        while(True):
            available, self.frame = self.cap.read()
            
            #frame = cv2.flip(frame,1)
            if not self.mouse_clicked : 
                cv2.imshow("Color Tracker",self.frame)   
            else : 
                frame_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                #cv2.imshow("frame_hsv",frame_hsv)
                mask = cv2.inRange(frame_hsv, self.color_lower_range, self.color_higher_range)
                #cv2.imshow("mask",mask)
                mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
                blur = cv2.GaussianBlur(mask,(3,3),0)
                gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
                edged = cv2.Canny(gray, 30, 200)
                img2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cv2.drawContours(self.frame, contours, -1, (0,255,0), 3)
                cv2.rectangle(self.frame,(5,5),(20,20),(self.b,self.g,self.r),-1)
                cv2.imshow("Color Tracker",self.frame)  
            		
            if cv2.waitKey(100) == 13:
                break
    

    def end(self) : 
        self.cap.release()
        cv2.destroyAllWindows()


CT = ColorTracker()
CT.start()
CT.end()