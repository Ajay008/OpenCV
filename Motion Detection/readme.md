# Motion Detection


### Description :
> * MotionDetection.py is a python program to detect motion by any object or even movement in camera in the video input.


### Working : 
> * It primarily works on BackgroungSubtractor function of OpenCV. 
> * After backgroundsubtraction, histogram is used to plot noise in the video frame.
> * If the noise in the video frame is grater than the threshold set, then a beep sound will be made.


### Limitation : 
> * Object without motion in a moving camera will also be considered as a motion. So, it can not be used to detect motion in moving camera.


### How to use ?
> Apart from defaults, you can
> * change the path variable in the ".py" file to select your video source or keep path=0 for primary webcam.
> * change the frequency variable to change the beep sound.
> * change threshold variable to set the noise tolerance.  

> To Run code, 
> * open command prompt and type "python MotionDetection.py" 
> * press Return/Enter key to exit.
	

### Prerequisites : 
> * Python 3.5
> * OpenCV 3.3
> * A Computer with a webcam or a video file


### Author :
> * Ajay Chaudhary

