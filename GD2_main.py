from Touch_Detector import Touch_Detector
import cv2
from GD2 import *

print("in gesture detector2")

grayscale_threshold = 130
touch_detector = Touch_Detector(grayscale_threshold=grayscale_threshold, width_height_ratio_threshold=0.3,
                                min_touch_area=500,
                                max_touch_area=7000)


def change_grayscale_threshold(x):
    touch_detector.grayscale_threshold = x


def change_min_area_threshold(x):
    touch_detector.min_touch_area = x


def change_max_area_threshold(x):
    touch_detector.max_touch_area = x


# gesture_detector = Gesture_Detector()
camera_port = "out2.avi"
camera = cv2.VideoCapture(camera_port)

cv2.namedWindow('image')
cv2.createTrackbar('GrayscaleMinValue', 'image', 0, 255, change_grayscale_threshold)
cv2.setTrackbarPos('GrayscaleMinValue', 'image', grayscale_threshold)
cv2.createTrackbar('Min Area', 'image', 10, 1000, change_min_area_threshold)
cv2.setTrackbarPos('Min Area', 'image', 500)
cv2.createTrackbar('Max Area', 'image', 10, 10000, change_max_area_threshold)
cv2.setTrackbarPos('Max Area', 'image', 7000)

gd2 = GD2()
while True:
    ok, frame = camera.read()
    if ok:
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ellipses = touch_detector.get_touch_ellipses(gray_frame)
        gd2.add_ellipses(ellipses)
        gesture = gd2.detect_gesture()
        if gesture is not Gestures.NO_GESTURE:
            print(gesture)
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
        image = touch_detector.visualize(ellipses=ellipses, image=rgb_frame)
        cv2.imshow("image", image)
        cv2.moveWindow("image", 1, 1)
        cv2.waitKey(1)