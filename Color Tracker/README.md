# Color Tracker


### Description :
> * Color Tracker can be used to highlight the selected color in the video.

### Working : 
> * The selected color is converted from BGR colorspace to HSV colorspace and a range for selected color is set.
> * Then we filter out the color from the video frame in the selected range.
> * And draw edges around the filterd color in the video frame.

### How to use ?
> * You can change the path variable in the ".py" file to select your video source or keep path=0 for primary webcam.

> To Run code, 
> * open command prompt and type "python ColorTracker.py"
> * click on any color on the video to select color
> * the selected color will be highlighted in all the coming frames of the video. 
> * press Return/Enter key to exit.
	

### Prerequisites : 
> * Python 3.5
> * OpenCV 3.3
> * A Computer with a webcam or a video file


### Author :
> * Ajay Chaudhary

