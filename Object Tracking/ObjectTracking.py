import numpy as np
import cv2
import math

# Set parameters for ShiTomasi corner detection
feature_params = dict(maxCorners = 500, qualityLevel = 0.3, minDistance = 7, blockSize = 7)
# Set parameters for lucas kanade optical flow
lucas_kanade_params = dict(winSize  = (15,15), maxLevel = 2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

class ObjectTracking(object) : 

    #path = './ball.mp4'
    path = 0
    draw_keypoints_enabled = True
    draw_bounding_rect_enabled = False
    interval = 20
    keypoint_accuracy = 0.50
    bounding_rect_accuracy = 0.90
    object_detection_accuracy = 0.80

    cap = cv2.VideoCapture(path)
    prev_frame = None
    prev_gray = None
    prev_points = []
    new_points = []
    mask = None
    tracker_enabled = False
    click_count = 0
    top_left = (0,0)
    bottom_right = (0,0)
    frame = None
    frame_gray = None
    selected_image = None
    selected_image_gray = None
    scan_count = 0
    find_keypoints_called = 0
    initial_keypoints = 0
    bounding_rect_top_left = (0,0)
    bounding_rect_bottom_right = (0,0)
    coords = []
    error = None
    rect_point1 = (0,0)
    rect_point2 = (0,0)
    find_selected_image_keypoints = False
    kp2, des2 = None, None
 
    def __init__(self):
        # Take first frame and find points in it
        _, self.prev_frame = self.cap.read()
        self.prev_gray = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)
        self.prev_points = np.asarray(self.prev_points, dtype=np.float32).reshape(-1,1,2)
        self.new_points = np.asarray(self.new_points, dtype=np.float32).reshape(-1,1,2)
        
        cv2.namedWindow('Object Tracking')
        cv2.setMouseCallback('Object Tracking', self.select_roi)


    def select_roi(self, event, x, y, flags, params) :
        if(self.click_count == 1) :
            self.rect_point2 = (x,y)
        if event == cv2.EVENT_LBUTTONDOWN and self.click_count < 2:
            self.click_count += 1      
            if self.click_count == 1 : 
                self.top_left = (x,y)
                self.rect_point1 = self.top_left
            elif self.click_count == 2 :
                if x < self.top_left[0] or y < self.top_left[1] :
                    self.click_count -= 1
                else : 
                    self.bottom_right = (x,y)
                    self.selected_image = self.frame[self.top_left[1]:self.bottom_right[1], self.top_left[0]:self.bottom_right[0], :]
                    self.selected_image_gray = cv2.cvtColor(self.selected_image, cv2.COLOR_BGR2GRAY)
                    cv2.imshow("selected_image",self.selected_image)
                    self.find_selected_image_keypoints = True
                    self.find_keypoints()
                    if self.error is None :
                        self.tracker_enabled = True
                    self.find_selected_image_keypoints = False


    def find_keypoints(self):
        surf = cv2.xfeatures2d.SURF_create(400)
        kp1,des1=surf.detectAndCompute(self.frame_gray,None)
        
        if self.find_selected_image_keypoints : 
            self.kp2,self.des2=surf.detectAndCompute(self.selected_image_gray,None)
            #print(len(kp1), len(self.kp2))
            if len(self.kp2) < 3 :
                self.error = "No keypoints found, Try again."
                return
            else : 
                self.error = None

        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1,self.des2,k=2)

        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)


        list_kp1 = []
        #list_kp2 = []
        for mat in good:
            img1_idx = mat.queryIdx
            #img2_idx = mat.trainIdx
            (x1,y1) = kp1[img1_idx].pt
            #(x2,y2) = kp2[img2_idx].pt
            list_kp1.append((x1, y1))
            #list_kp2.append((x2, y2))

        self.prev_points = []
        self.prev_points = np.asarray(self.prev_points, dtype=np.float32).reshape(-1,2)
        for (x,y) in list_kp1 :
            x = np.float32(x)
            y = np.float32(y)
            self.prev_points = np.append(self.prev_points,[x,y])
        self.prev_points = self.prev_points.reshape(-1,1,2)


        if self.find_keypoints_called == 0 :
            self.find_keypoints_called += 1
            self.initial_keypoints = len(list_kp1)
        

    def find_bounding_rect_coords(self):
        coords_count = self.coords.shape[0]
        coords_x = [x for x,y in self.coords]
        coords_y = [y for x,y in self.coords]
        left = min(coords_x)
        right = max(coords_x)
        top = min(coords_y)
        bottom = max(coords_y)

        tolerance = coords_count * (1-self.bounding_rect_accuracy)
        while left < 640 :
            left += 10 
            temp = [x for x,y in self.coords if x<left]
            if len(temp) > tolerance :
                temp = [x for x,y in self.coords if x<left+10]
                left = max(temp)
                break
        
        while right > 0 :
            right -= 10 
            temp = [x for x,y in self.coords if x>right]
            if len(temp) > tolerance :
                temp = [x for x,y in self.coords if x>right-10]
                right = min(temp)
                break
        while top < 480 :
            top += 10 
            temp = [y for x,y in self.coords if y<top]
            if len(temp) > tolerance :
                temp = [y for x,y in self.coords if y<top+10]
                top = max(temp)
                break
        while bottom > 0 :
            bottom -= 10 
            temp = [y for x,y in self.coords if y>bottom]
            if len(temp) > tolerance :
                temp = [y for x,y in self.coords if y>bottom-10]
                bottom = min(temp)
                break
        self.bounding_rect_top_left = (int(left), int(top))
        self.bounding_rect_bottom_right = (int(right), int(bottom))
        




    def start(self) :    
        while(True):
            ret, self.frame = self.cap.read()
            self.frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            if ret :
                if self.tracker_enabled : #and self.prev_points is not None:
                    self.scan_count += 1 
                    self.prev_points = self.prev_points.reshape(-1,1,2)
                    
                    self.new_points, status, errors = cv2.calcOpticalFlowPyrLK(self.prev_gray, self.frame_gray, self.prev_points, None, **lucas_kanade_params)
                    
                    if self.new_points is not None: 
                        temp = self.new_points[status==1]
                        self.coords = temp.reshape(-1,2)
                        for x,y in self.coords:
                            if self.draw_keypoints_enabled : 
                                cv2.circle(self.frame, (int(x),int(y)), 3, (0,255,0),-1)
                        

                        if len(self.coords) > self.initial_keypoints * (1-self.object_detection_accuracy) :
                            if self.draw_bounding_rect_enabled : 
                                if len(self.coords) != 0 :
                                    self.find_bounding_rect_coords()
                                    cv2.rectangle(self.frame, self.bounding_rect_top_left , self.bounding_rect_bottom_right, (255,0,0), 2)
                            
                            coords_x_30 = [0] * (math.ceil(640/30) + 1)
                            coords_y_30 = [0] * (math.ceil(480/30) + 1)
                            for x,y in self.coords :
                                i, j = int(x/30), int(y/30)
                                coords_x_30[i] += 1
                                coords_y_30[j] += 1
                            center_x = coords_x_30.index(max(coords_x_30)) * 30 + 15
                            center_y = coords_y_30.index(max(coords_y_30)) * 30 + 15

                            cv2.line(self.frame,(center_x-10 ,center_y),(center_x+10 ,center_y),(255,0,0),2)
                            cv2.line(self.frame,(center_x ,center_y-10),(center_x ,center_y+10),(255,0,0),2)
                            cv2.circle(self.frame, (center_x, center_y), 15, (255,0,0), 2)
                            cv2.putText(self.frame,str(len(self.coords)),(0,20),cv2.FONT_HERSHEY_SIMPLEX,1,color = (200,50,75),thickness = 3)
                        else : 
                            cv2.putText(self.frame,"Object Not Found",(0,20),cv2.FONT_HERSHEY_SIMPLEX,1,color = (200,50,75),thickness = 3)    


                        self.prev_gray = self.frame_gray.copy()
                        self.prev_points = self.new_points.reshape(-1,1,2)

                      
                    cond_1 = self.new_points is None
                    cond_2 = self.prev_points[status==1].shape[0] < self.initial_keypoints * self.keypoint_accuracy
                    cond_3 = self.scan_count % self.interval == 0
                    if cond_1 or cond_2 or cond_3 :
                        self.find_keypoints()
                        self.error = None
                    if self.scan_count == 500 :
                        self.scan_count == 0
                
                error_free_frame = self.frame.copy()
                if self.error is not None : 
                    cv2.putText(self.frame, str(self.error), (0,20),cv2.FONT_HERSHEY_SIMPLEX,1,color = (200,50,75),thickness = 3)    

                frame_copy = self.frame.copy()
                if self.click_count == 1 and self.rect_point2[0] > self.rect_point1[0] and self.rect_point2[1] > self.rect_point1[1] : 
                    cv2.rectangle(frame_copy, self.rect_point1, self.rect_point2, (255,0,0), 2)
                    cv2.imshow('Object Tracking',frame_copy)
                else : 
                    cv2.imshow('Object Tracking',self.frame)

                key = cv2.waitKey(25)
                if key == ord('p'):
                    key2 = cv2.waitKey(25)
                    while key2 != ord('s'):
                        if key2 == ord('r') : 
                            self.frame = error_free_frame
                            key = key2
                        elif key2 == 13 :
                            key = 13
                            break

                        if self.click_count == 1 and self.rect_point2[0] > self.rect_point1[0] and self.rect_point2[1] > self.rect_point1[1] : 
                            frame_copy = self.frame.copy()
                            cv2.rectangle(frame_copy, self.rect_point1, self.rect_point2, (255,0,0), 2)
                            cv2.imshow('Object Tracking',frame_copy)
                        else : 
                            cv2.imshow('Object Tracking',self.frame)
                        key2 = cv2.waitKey(25)
                        continue
                if key == ord('r') : 
                    self.click_count = 0
                    self.tracker_enabled = False
                    self.error = None
                if key == 13: #13 is the Enter Key
                    break
                

    def end(self) :
        cv2.destroyAllWindows()
        self.cap.release()


OT = ObjectTracking()
OT.start()
OT.end()