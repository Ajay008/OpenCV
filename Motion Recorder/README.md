# Motion Recorder

[Watch on Youtube](https://www.youtube.com/watch?v=EmiyIXlw21w)

### Description :
> * Storing complete recordings of surveillance can consume a lot of storage. The frames of video recordings that are steady and does not have any movement can be discarded. We need to store only those part of video that has any motion. This program can be used to achieve this goal.


### Working : 
> * It works on BackgroungSubtractor function of OpenCV. 
> * After backgroundsubtraction, histogram is used to find amount of motion in the video frame.
> * If the motion in the video frame is grater than the threshold set, then those frames are added to final video.


### Limitation : 
> * It can not be used with a moving camera.

### How to use ?
> Apart from defaults, you can
> * change the path variable in the ".py" file to select your video source or keep path=0 for primary webcam.
> * change threshold variable to set the amount of motion to record.

[Watch on Youtube](https://www.youtube.com/watch?v=EmiyIXlw21w)
> To Run code, 
> * open command prompt and type "python MotionRecorder.py" 
> * press Return/Enter key to exit.
	

### Prerequisites : 
> * Python 3.5
> * OpenCV 3.3
> * A Computer with a webcam or a video file


### Author :
> * Ajay Chaudhary

