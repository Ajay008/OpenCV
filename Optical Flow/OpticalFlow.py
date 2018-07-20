import numpy as np
import cv2

# Set parameters for lucas kanade optical flow
lucas_kanade_params = dict(winSize  = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

class OpticalFlow() : 
    path = 0
    #path = '../videos/motion.mp4'

    cap = cv2.VideoCapture(path)
    prev_frame = None
    prev_gray = None
    prev_points = []
    new_points = []
    mask = None
    tracker_enabled = False

    def __init__(self):
        # Take first frame and find points in it
        _, self.prev_frame = self.cap.read()
        self.prev_gray = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
        self.prev_points = np.asarray(self.prev_points, dtype=np.float32).reshape(-1,1,2)
        self.new_points = np.asarray(self.new_points, dtype=np.float32).reshape(-1,1,2)
        
        cv2.namedWindow('Optical Flow')
        cv2.setMouseCallback('Optical Flow', self.draw_circle)


    def draw_circle(self, event, x, y, flags, params) :
        if event == cv2.EVENT_LBUTTONDOWN :      
            x = np.float32(x)
            y = np.float32(y)
            self.prev_points = np.append(self.prev_points,[x,y])
            self.tracker_enabled = True

    def start(self) :    
        while(True):
            ret, frame = self.cap.read()
            if ret :
                if self.tracker_enabled : 
                    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    self.prev_points = self.prev_points.reshape(-1,1,2)
                    self.new_points, status, errors = cv2.calcOpticalFlowPyrLK(self.prev_gray, frame_gray, self.prev_points, None, **lucas_kanade_params)
                    temp_new = self.new_points[status==1]
                    temp_new = temp_new.reshape(-1,2)
                    for a,b in temp_new:
                        frame = cv2.circle(frame, (int(a),int(b)), 3, (0,255,0),-1)
                    cv2.putText(frame,str(len(temp_new)),(0,20),cv2.FONT_HERSHEY_SIMPLEX,1,color = (200,50,75),thickness = 3)

                    self.prev_gray = frame_gray.copy()
                    self.prev_points = self.new_points.reshape(-1,1,2)

                #frame = cv2.flip(frame,1)
                cv2.imshow('Optical Flow',frame)
                key = cv2.waitKey(25)
                if key == 13 : 
                    break
                elif key == ord('p'):
                    while cv2.waitKey(25) != ord('s'):
                        continue


    def end(self) :
        cv2.destroyAllWindows()
        self.cap.release()


OF = OpticalFlow()
OF.start()
OF.end()