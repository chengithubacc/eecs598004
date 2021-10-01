import cv2
from Touch_Detector import Touch_Detector
import random
import collections
from GD2 import process_gesture

def change_grayscale_threshold(x):
    touch_detector.grayscale_threshold = x
def change_min_area_threshold(x):
    touch_detector.min_touch_area = x
def change_max_area_threshold(x):
    touch_detector.max_touch_area = x
# Initialize MultiTracker

touch_detector = Touch_Detector(grayscale_threshold=200, width_height_ratio_threshold=0.3, min_touch_area=500,
                                max_touch_area=7000)
camera_port = 1
camera = cv2.VideoCapture(camera_port)
camera = cv2.VideoCapture("out.avi")
cv2.namedWindow('image')
cv2.createTrackbar('GrayscaleMinValue', 'image', 0, 255, change_grayscale_threshold)
cv2.setTrackbarPos('GrayscaleMinValue', 'image', 200)
cv2.createTrackbar('Min Area', 'image', 10, 1000, change_min_area_threshold)
cv2.setTrackbarPos('Min Area', 'image', 500)
cv2.createTrackbar('Max Area', 'image', 10, 10000, change_max_area_threshold)
cv2.setTrackbarPos('Max Area', 'image', 7000)

trackerType = "CSRT"
multiTracker = cv2.legacy.MultiTracker_create()
is_tracking = False

def check_if_is_tracking(box, tracking_boxes,overlap_x_safe_region=10,overlap_y_safe_region=10):
    xi, yi, wi, hi = box
    is_new = True
    for box in tracking_boxes:
        x, y, w, h = box
        is_far_enough = ((x-xi)**2 + (y-yi)**2)>800
        x_ub = x+w+overlap_x_safe_region
        x_lb = x-overlap_x_safe_region
        y_ub = y+h+overlap_y_safe_region
        y_lb = y-overlap_y_safe_region
        xi_ub = xi+wi+overlap_x_safe_region
        xi_lb = xi-overlap_x_safe_region
        yi_ub = yi+hi+overlap_y_safe_region
        yi_lb = yi-overlap_y_safe_region
        is_not_overlap = not ((x_lb<xi<x_ub and y_lb<yi<y_ub) or (xi_lb<x<xi_ub and yi_lb<y<yi_ub))
        #print("overlap 1: ",is_not_overlap,(x_lb<xi<x_ub and y_lb<yi<y_ub),(xi_lb<x<xi_ub and yi_lb<y<yi_ub))
        is_not_overlap &= not ((x_lb<xi+wi<x_ub and y_lb<yi+hi<y_ub) or (xi_lb<x+w<xi_ub and yi_lb<y+h<yi_ub))
        #print("overlap 2: ",is_not_overlap)
        # if not is_not_overlap:
        #     print(box, (xi,yi,wi,hi))
        is_new &= (is_not_overlap and is_far_enough)
        if not is_new:
            break
    return is_new

tracking_boxes = []
buffer_size = 40
max_size = 100
bbox_history = {i:collections.deque(buffer_size*[None],buffer_size) for i in range(max_size)}
colors = []
for i in range(max_size):
    colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
while True:
    ok, frame = camera.read()
    if ok:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ellipses = touch_detector.get_touch_ellipses(gray_frame)
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
        for ellipse in ellipses:
            x, y = ellipse[0]
            w, h = ellipse[1]
            r = ellipse[2]
            x,y,w,h = [int(i) for i in [x-w/2,y-h/2,w,h]]
            box_tmp = (x,y,w,h)
            is_new = check_if_is_tracking(box_tmp, tracking_boxes)
            if is_new:
                multiTracker.add(cv2.legacy.TrackerKCF_create(), frame, box_tmp)
        success, tracking_boxes = multiTracker.update(frame)
        if len(tracking_boxes)==0:
            # clear up
            del multiTracker
            multiTracker = cv2.legacy.MultiTracker_create()
            del bbox_history
            bbox_history = {i:collections.deque(buffer_size*[None],buffer_size) for i in range(max_size)}
        for i, newbox in enumerate(tracking_boxes):
            x,y,w,h = newbox
            bbox_history[i].append(newbox)
            p1 = (int(newbox[0]), int(newbox[1]))
            p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
            cv2.rectangle(rgb_frame, p1, p2, colors[i], 2, 1)
        image = touch_detector.visualize(ellipses=ellipses, image=rgb_frame)
        pos_dict = process_gesture(bbox_history,buffer_size=buffer_size)
        if len(pos_dict):
            print(pos_dict)
            print(bbox_history[0])
            # del multiTracker
            # multiTracker = cv2.legacy.MultiTracker_create()
            del bbox_history
            bbox_history = {i:collections.deque(buffer_size*[None],buffer_size) for i in range(max_size)}

        cv2.imshow("image", image)
        cv2.waitKey(1)


# while cap.isOpened():
#   success, frame = cap.read()
#   if not success:
#     break
#
#   # get updated location of objects in subsequent frames
#   success, boxes = multiTracker.update(frame)
#
#   # draw tracked objects
#   for i, newbox in enumerate(boxes):
#     p1 = (int(newbox[0]), int(newbox[1]))
#     p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
#     cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
#
#   # show frame
#   cv2.imshow('MultiTracker', frame)
#
#   # quit on ESC button
#   if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
#     break