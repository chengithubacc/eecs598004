import cv2
import datetime
from Touch_Detector import Touch_Detector
from Gesture_Detector import Gesture_Detector


def change_grayscale_threshold(x):
    touch_detector.grayscale_threshold = x
def change_min_area_threshold(x):
    touch_detector.min_touch_area = x
def change_max_area_threshold(x):
    touch_detector.max_touch_area = x

if __name__ == '__main__':
    grayscale_threshold = 150
    touch_detector = Touch_Detector(grayscale_threshold=grayscale_threshold, width_height_ratio_threshold=0.3, min_touch_area=500,
                                    max_touch_area=7000)
    gesture_detector = Gesture_Detector()
    camera_port = 1
    camera = cv2.VideoCapture(camera_port)


    cv2.namedWindow('image')
    cv2.createTrackbar('GrayscaleMinValue', 'image', 0, 255, change_grayscale_threshold)
    cv2.setTrackbarPos('GrayscaleMinValue', 'image', grayscale_threshold)
    cv2.createTrackbar('Min Area', 'image', 10, 1000, change_min_area_threshold)
    cv2.setTrackbarPos('Min Area', 'image', 500)
    cv2.createTrackbar('Max Area', 'image', 10, 10000, change_max_area_threshold)
    cv2.setTrackbarPos('Max Area', 'image', 7000)

    prev_ellipses = [(0,0),(0,0),0]
    curr_patience = dict([('up', 0), ('down', 0), ('left', 0), ('right', 0), ('three', 0), ('four', 0), ('pinch', 0)])
    latest_time = datetime.datetime.now()
    while True:
        ok, frame = camera.read()
        if ok:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ellipses = touch_detector.get_touch_ellipses(gray_frame)
            rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
            image = touch_detector.visualize(ellipses=ellipses, image=rgb_frame)
            cv2.imshow("image",image)
            cv2.moveWindow("image", 1,1);
            curr_patience = gesture_detector.track_movement(ellipses, prev_ellipses, curr_patience, latest_time)
            # print(curr_patience)
            latest_time, command = gesture_detector.decide_action(curr_patience, latest_time)
            print(command)
            cv2.waitKey(80)
            prev_ellipses = ellipses
