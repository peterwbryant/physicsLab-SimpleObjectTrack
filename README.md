# physicsLab-SimpleObjectTrack
OpenCV-based python scripts for object tracking, initially written specifically for tracking **projectiles** and **pendulums**.
---

## Required Libraries
1. numpy
2. opencv-contrib-python

## Script Usage
Edit the file ```main.py``` in two places, both near the top of the file:
1. set ```analysis``` variable to one of
    1. ```'projectile'``` for the **projectile** analysis, in which the user must click the two ends of an object of unit length visible in the initial frame.
    2. ```'pendulum'``` for the **pendulum analysis**, in which, in addition to two clicks at the ends of an object of unit length, the user must click a third time on the pivot point of the pendulum
3. set ```infile``` to the name of the input video file

## Runtime
Two windows will open with the initial frame from the input video file.
1. First, in the window titled "Image Calibration," click
    1. twice for the **projectile** analysis: once at one end of the reference object of unit length, and once at the other end
    2. three times for the **pendulum** analysis: twice as for the pendulum analysis, and a third time at the pivot location of the pendulum.

    Note that additional clicks will be ignored.

2. Second, in the window titled "ROI", drag a box around the object to be tracked.


## Best Practices
1. Be sure the object is visible in all frames and not obscured in the initial frame.
2. Eliminate features in the background if possible.
