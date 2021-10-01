import threading
import time

import cv2
import datetime
from Touch_Detector import Touch_Detector



gestures_command = dict([('wait', 0), ('up', 1), ('down', 2), ('left', 3), ('right', 4), ('three', 5), ('four', 6), ('pinch', 7)])

class Gesture_Detector:
    def __init__(self, max_width=3, min_height=7, max_height=3, min_width=7, pinch_width=2):
        print("in gesture detector1")
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.min_width = min_width
        self.pinch_width = pinch_width
        self.patience = dict([('up', 7), ('down', 7), ('left', 7), ('right', 7), ('three', 1), ('four', 1), ('pinch', 2)])

        self._t_effector = threading.Thread(target=self.initGestureDetector)
        self._t_effector.daemon = True
        # "before the start`"
        self._t_effector.start()

        self.command = None
        self.new_data = False
        self.lastGet = time.time()
        self.rtnFlag = False

    def getGesture(self):
        # if self.new_data == True:
        #     if time.time() - self.lastGet < 2:
        #         print("t1: {}  t2: {}".format(time.time(), self.lastGet))
        #         print("less than 2")
        #         return 0
        #     self.new_data = False
        # self.lastGet = time.time()
        return self.command

    def track_movement(self, ellipses, prev_ellipses, curr_patience, latest_time):
        """

        :param ellipses: a list of valid ellipses at current time stamp
        :param prev_ellipses: a list of valid ellipses at the previous time stamp
        :param curr_patience: a dictionary of patience values involving up/down, left/right, pinch movement
        :return:
        """

        ts = datetime.datetime.now()
        duration = ts - latest_time
        duration = duration.total_seconds()

        if duration < 2:
            return curr_patience

        # Up/down, left/right
        if len(ellipses) == 1 and len(prev_ellipses) == 1:
            x1, y1 = prev_ellipses[0][0]
            x2, y2 = ellipses[0][0]
            # Upside down
            if abs(x1-x2) < self.max_width and abs(y1-y2) > self.min_height:
                if y1 > y2:
                    curr_patience['up'] += 1
                else:
                    curr_patience['down'] += 1
            elif abs(y1-y2) < self.max_height and abs(x1-x2) > self.max_width:
                if x1 > x2:
                    curr_patience['right'] += 1
                else:
                    curr_patience['left'] += 1

        # Three fingers
        if len(ellipses) == 3 and len(prev_ellipses) == 3:
            curr_patience['three'] += 1

        # Four fingers
        if len(ellipses) == 4 and len(prev_ellipses) == 4:
            curr_patience['four'] += 1

        # pinch
        if len(ellipses) == 2 and len(prev_ellipses) == 2:
            x1, y1 = prev_ellipses[0][0]
            x2, y2 = ellipses[0][0]
            x1p, y1p = prev_ellipses[1][0]
            x2p, y2p = ellipses[1][0]
            if abs(x1-x2) > self.pinch_width and abs(x1p-x2p) > self.pinch_width and abs(y1-y2) > self.pinch_width and abs(y1p-y2p) > self.pinch_width:
                curr_patience['pinch'] += 1

        return curr_patience

    def decide_action(self, curr_patience, latest_time):
        """r

        :param curr_patience:
        :return: latest action time
        """
        ts = datetime.datetime.now()

        for key in self.patience:
            if self.patience[key] <= curr_patience[key]:
                # print('Time {}: {}'.format(ts, key))
                for k in self.patience:
                    curr_patience[k] = 0
                self.rtnFlag = True
                return ts, gestures_command[key]
        # else:
        #     if self.rtnFlag:
        #         for k in self.patience:
        #             curr_patience[k] = 0

        return latest_time, gestures_command['wait']

    def initGestureDetector(self):
        print("in gesture detector2")

        grayscale_threshold = 170
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
        camera_port = 1
        camera = cv2.VideoCapture(camera_port)

        cv2.namedWindow('image')
        cv2.createTrackbar('GrayscaleMinValue', 'image', 0, 255, change_grayscale_threshold)
        cv2.setTrackbarPos('GrayscaleMinValue', 'image', grayscale_threshold)
        cv2.createTrackbar('Min Area', 'image', 10, 1000, change_min_area_threshold)
        cv2.setTrackbarPos('Min Area', 'image', 500)
        cv2.createTrackbar('Max Area', 'image', 10, 10000, change_max_area_threshold)
        cv2.setTrackbarPos('Max Area', 'image', 7000)

        prev_ellipses = [(0, 0), (0, 0), 0]
        curr_patience = dict(
            [('up', 0), ('down', 0), ('left', 0), ('right', 0), ('three', 0), ('four', 0), ('pinch', 0)])
        latest_time = datetime.datetime.now()
        while True:
            ok, frame = camera.read()
            if ok:
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                ellipses = touch_detector.get_touch_ellipses(gray_frame)
                rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
                image = touch_detector.visualize(ellipses=ellipses, image=rgb_frame)
                cv2.imshow("image", image)
                cv2.moveWindow("image", 1, 1)
                curr_patience = self.track_movement(ellipses, prev_ellipses, curr_patience, latest_time)
                latest_time, self.command = self.decide_action(curr_patience, latest_time)
                self.new_data = True
                # print(command)
                cv2.waitKey(80)
                prev_ellipses = ellipses

if __name__ == '__main__':
    GD = Gesture_Detector()
    while True:
        print(GD.getGesture())
        time.sleep(0.08)





