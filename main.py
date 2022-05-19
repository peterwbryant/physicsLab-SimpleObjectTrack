import cv2
import csv
import numpy as np

# Choose analysis type.
#   'projectile' requires two clicks at the ends of a unit length standard
#   'pendulum' requires a third click at the pivot point
# -----------------------------------
# analysis = 'projectile'
analysis = 'pendulum'

# Input file name
infile = 'videos/inputFile.mp4'
infile = 'videos/inputBalloon.mp4'

refPt = []


# click event function
def click_event(event, xx, yy, flags, param):
    global refPt
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt.append([xx, yy])
        font = cv2.FONT_HERSHEY_SIMPLEX
        strXY = str(xx) + ", " + str(yy)
        cv2.putText(frame, strXY, (xx, yy), font, 0.5, (255, 255, 0), 2)
        cv2.imshow("Image Calibration", frame)


# record x and y locations
xloc = []
yloc = []

# Choose a tracking algorithm
# tracker = cv2.TrackerKCF_create()
# tracker = cv2.TrackerMIL_create()
tracker = cv2.TrackerCSRT_create()

video = cv2.VideoCapture(infile)
ok, frame = video.read()

# image sizes
xsize = frame.shape[1]
ysize = frame.shape[0]

# frames per second
fps = video.get(cv2.CAP_PROP_FPS)

# get both ends of unit marker
cv2.namedWindow('Image Calibration')
cv2.moveWindow('Image Calibration', -150, 0)  # so both windows are visible on small monitors
cv2.imshow("Image Calibration", frame)
print("First click one side of standard unit.")
cv2.setMouseCallback("Image Calibration", click_event)
print("Then click the other side of standard unit.")
cv2.setMouseCallback("Image Calibration", click_event)
print("For a pendulum, click the pivot point.")
cv2.setMouseCallback("Image Calibration", click_event)

# drag over region (object) of interest
bbox = cv2.selectROI(frame)

ok = tracker.init(frame, bbox)

# prepare to write processed video
out = cv2.VideoWriter('processed.mp4',
                      cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                      fps, (xsize, ysize))

while True:
    ok, frame = video.read()
    if not ok:
        break
    ok, bbox = tracker.update(frame)
    if ok:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 1)
        xloc.append(x + w / 2.)
        yloc.append(ysize - (y + h / 2.))
    else:
        cv2.putText(frame, 'Error', (100, 0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0XFF == 27:
        break
    out.write(frame)
cv2.destroyAllWindows()
out.release()

# scale to physical units
pixPerUnit = np.sqrt((refPt[0][0] - refPt[1][0]) ** 2 + (refPt[0][1] - refPt[1][1]) ** 2)

# pivot point, if there is one
if analysis == 'pendulum':
    xPiv = refPt[2][0]
    yPiv = ysize - refPt[2][1]

# data processing
if analysis == 'projectile':
    # min y is y = 0
    xv = np.asarray(xloc) / pixPerUnit
    yv = (np.asarray(yloc) - np.min(np.asarray(yloc))) / pixPerUnit
elif analysis == 'pendulum':
    # x = 0 at min y
    yv = (np.asarray(yloc) - yPiv) / pixPerUnit
    xv = (np.asarray(xloc) - xPiv) / pixPerUnit
else:
    # x positive right, y positive left
    xv = np.asarray(xloc) / pixPerUnit
    yv = np.asarray(yloc) / pixPerUnit

# time
t = np.arange(0, len(xv) / fps, 1 / fps)

with open('objectTrajectory.csv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(zip(t.tolist(), xv.tolist(), yv.tolist()))
