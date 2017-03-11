## Project Writeup

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./examples/undistort_output.png "Undistorted"
[image2]: ./test_images/distortion_correction.png "Road Transformed"
[image3]: ./examples/binary_combo_example.png "Binary Example"
[image4]: ./examples/warped_straight_lines.png "Warp Example"
[image5]: ./examples/color_fit_lines.png "Fit Visual"
[image6]: ./examples/example_output.png "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points
###Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
###Writeup / README

####1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  

You're reading it!
###Camera Calibration

####1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the the file called `calibrate.py`.  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

###Pipeline (single images)

####1. Provide an example of a distortion-corrected image.
To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image2]
####2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.
The code for this step is contained in the the file called `thresholding.py`
I use the combination of the following for thresholding-
* Color space - Saturation (S) thresholding in HLS color space and Red (R) thresholding in RGB color space
* Sobel gradient thesholding in X direction
Then I combined the results of the three to generate a more robust thresholding.

![alt text][image3]

####3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.
The code for this step is contained in the the file called `transform.py`
The code for my perspective transform includes a function called `transform_to_top_down()`, The `transform_to_top_down()` function takes as inputs an image, and using pre-defined source and destination points, performs the perspective transform.  I chose the hardcode the source and destination points in the following manner:

```
default_src_points = np.float32([[585.714, 456.34],
                                 [699.041, 456.34],
                                 [1029.17, 667.617],
                                 [290.454, 667.617]])

default_dst_points  = np.float32([[300, 70],
                                  [1000, 70],
                                  [1000, 600],
                                  [300, 600]])

```
I verified that my perspective transform was working as expected by drawing the source and destination points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

####4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?
The code for this step is contained in the the file called `detection.py`
Lane line detection is done using the sliding windows technique explained in the course. The sum of all the line points detect in the thresholding phase is taken for the bottom half of the image. This let's us detect where the two lane lines are approximately. Using this approximation, we then find all the nonzero values inside a window, and store those points as points for the lane line. We slide the window up, and repeat finding nonzero values. When the sliding window reaches the top of the image, we fit a parabola to the points that were detected. This polynomial can be used to calculate the lane line values at any point.

![alt text][image5]

####5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.
The code for this step is contained in the the file called `lane.py`
fit = np.polyfit(xs, ys) # using the xs and ys found during detection
p   = np.poly1d(fit)     # polynomial helper function
p1  = np.polyder(p)      # first derivative of out polynomial
p2  = np.polyder(p, 2)   # second derivative of our polynomial

y is the point at which you'd like to find the curvature
((1 + (p1(y)**2))**1.5) / np.absolute(p2(y))

Assuming the camera is mounted in the center of the car, the distance to the center of the lane can be calculated by find the difference from the center of the lanes, to the center of the image.

####6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.
The code for this step is contained in the the file called `pipeline.py`
Here is an example of my result on a test image:

![alt text][image6]

---

###Pipeline (video)

####1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).
The code for this step is contained in the the file called `convert_video.py`

Here's a [link to my video result](./project_video.mp4)

---

###Discussion

####1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Challenges:
Identifying features and thresholds.

Recommendations:
The algorithm is dependent on the features chosen and the thresholds selected. This makes it prone to error if the conditions on the road differ vastly from the data used for calculations. Better approach would be to use Deep Learning for identifying the lanes.

