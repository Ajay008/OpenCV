# Object Tracking


### Description :
> * Object Tracking in this program is done by using 2 algorithms 
>   1) Lucas Kanade Optical Flow Algorithm
>   2) SURF Algorithm for feature extraction

### Working : 
> * After the object is selected, feature extraction algorithm SURF is applied on image of selected object.
> * Features of image of selected object is compared with features of all the coming frames by Flann Based Matcher.
> *  If the match is found the object is marked.
> * Once the object is selected, it can be detected even if it is rotated or if the distance of the object is changed.


### Limitation : 
> * It may give poor results if the lightening conditions are not good or when the object does not have good features or when object has similar features as its background.


### How to use ?
> Apart from defaults, you can
> * change the path variable in the ".py" file to select your video source or keep path=0 for primary webcam.
> * change the draw_keypoints_enabled variable if to True of False
if you want to see features in the output.
> * change the various accuracy varibles to acquires desired result.

> To Run code, 
> * open command prompt and type "python ObjectTracking.py"
> * (optional) press 'p' on keyboard to pause video. 
> * draw a rectangle around the object in the video frame using your mouse.
> * (optional) if you pressed 'p' earlier then press 's' on keyboard to start video.
> * (optional) press 'r' on keyboard to reset the selected image. so that you can select a new object to track
> * the object will be marked if found in the coming frames.
> * press Return/Enter key to exit.

> Try this,
> * Place the front page of any book or a page with cartoons on it infront of the webcam. (Because the objects will be unique and more features will be extracted and hence it will be tracked with higher accuracy.) 
	

### Prerequisites : 
> * Python 3.5
> * OpenCV 3.3
> * A Computer with a webcam or a video file


### Author :
> * Ajay Chaudhary

