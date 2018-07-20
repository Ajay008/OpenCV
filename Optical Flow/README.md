# Optical Flow Object Tracking


### Description :
> * This program is an implementation of Lucas Kanade Optical Flow algorithm.


### Working :  
> * A set of points from previous frame is given as an input to the lucas kanade optical flow function and it returns a set of new points for the new frame.
> * Some of new points with more error are removed and others are plotted in the new frame.


### Limitation : 
> * Once we loose the track of points from the previous frame, those points can not be obtained back.

### How to use ?
> Apart from defaults, you can
> * change the path variable in the ".py" file to select your video source or keep path=0 for primary webcam. 

> To Run code, 
> * open command prompt and type "python OpticalFlow.py" 
> * plot the points on the object in the video frame you want to track by mouse.
> * press Return/Enter key to exit.

> Try this :
> * Run the program and in the webcam view, plot points on your face and move your face, the points will move along your face where they were plotted. 


### Prerequisites : 
> * Python 3.5
> * OpenCV 3.3
> * A Computer with a webcam or a video file

### Author :
> * Ajay Chaudhary
