import math
from enum import Enum

import cv2


class Gestures(Enum):
    NO_GESTURE=0
    THREE_PRESS_HOLD=1
    FOUR_PRESS_HOLD=2
    SWIPE_UP=3
    SWIPE_DOWN=4
    SWIPE_LEFT=5
    SWIPE_RIGHT=6
    PINCH=7
    PALM_PRESSING=8

class Single_Gestures(Enum):
    NO_GESTURE=0
    PRESS_HOLD=1
    SWIPE=2

class GD2:
    def __init__(self, min_wait_frame=6, min_prep_wait_frame=3, pinch_x_min_dist=2,
                 pinch_y_min_dist=4, swipe_min_dist=50, palm_pressing_threshold=640 * 480 / 5,
                 palm_pressing_missing_threshold=30, debug_mode=True):
        self.history = Ellipse_History()
        self.min_wait_frame = min_wait_frame
        self.min_prep_wait_frame = min_prep_wait_frame
        self.pinch_x_min_dist = pinch_x_min_dist
        self.pinch_y_min_dist = pinch_y_min_dist
        self.debug_mode = debug_mode
        self.swipe_min_dist = swipe_min_dist
        self.palm_pressing_threshold = palm_pressing_threshold
        self.palm_pressing_missing_threshold = palm_pressing_missing_threshold
        self.palm_pressing_status = {"is_triggered":False,
                                     "not_pressed_ct":0}

    def print_single_gestures(self):
        printed = False
        for i,d in self.history.history.items():
            printed = True
            print(i,": ",d["gesture"],end=" ")
        if printed:
            print()

    def add_ellipses(self,list_of_ellipses):
        self.history.add_many(list_of_ellipses)

    def detect_palm_pressing(self, thresholded_img, hist):
        for i,d in hist.items():
            if d["is_triggered"]:
                return Gestures.NO_GESTURE
        white_pixels_ct = cv2.countNonZero(thresholded_img)
        is_pressing = white_pixels_ct > self.palm_pressing_threshold
        gesture = Gestures.NO_GESTURE
        if is_pressing:
            if not self.palm_pressing_status["is_triggered"]:
                gesture = Gestures.PALM_PRESSING
                self.palm_pressing_status["is_triggered"] = True
        else:
            self.palm_pressing_status["not_pressed_ct"]+=1
            if self.palm_pressing_status["not_pressed_ct"]>self.palm_pressing_missing_threshold:
                self.palm_pressing_status["not_pressed_ct"]=0
                self.palm_pressing_status["is_triggered"] = False
        return gesture

    def detect_gesture(self, thresholded_img):
        hist = self.history.history
        gesture = self.detect_palm_pressing(thresholded_img,hist)
        if gesture == gesture.NO_GESTURE and not self.palm_pressing_status["is_triggered"]:
            for i,d in hist.items():
                if not d["is_triggered"]:
                    if len(d["history"])>self.min_wait_frame:
                        single_hist = d["history"]
                        gesture, value = self.process_single_gesture(single_hist)
                        hist[i]["gesture"] = gesture
                        hist[i]["value"] = value
                        hist[i]["is_in_detect_state"] = True
                        hist[i]["is_in_prep_state"] = True
                    elif len(d["history"])>self.min_prep_wait_frame:
                        single_hist = d["history"]
                        gesture, value = self.process_single_gesture(single_hist)
                        hist[i]["gesture"] = gesture
                        hist[i]["value"] = value
                        hist[i]["is_in_prep_state"] = True

            gesture = self.process_gesture(hist)
        #self.print_single_gestures()
        return gesture


    def process_gesture(self,hist):
        final_gesture = Gestures.NO_GESTURE
        hold_ct = 0
        hold_prep_ct = 0
        holds = {}
        holds_prep = {}
        swipe_ct = 0
        swipe_prep_ct = 0
        swipes = {}
        swipes_prep = {}
        for i,d in hist.items():
            if d["is_triggered"]:
                return Gestures.NO_GESTURE
            if not d["is_triggered"]:
                if d["gesture"] == Single_Gestures.PRESS_HOLD:
                    hold_prep_ct+=1
                    holds_prep[i] = d["value"]
                    if d["is_in_detect_state"]:
                        hold_ct+=1
                        holds[i] = d["value"]
                elif d["gesture"] == Single_Gestures.SWIPE:
                    swipe_prep_ct+=1
                    swipes_prep[i] = d["value"]
                    if d["is_in_detect_state"]:
                        swipe_ct+=1
                        swipes[i] = d["value"]

        # if self.debug_mode:
        #     if len(hist)>0:
        #         print("Hold: ", hold_ct, hold_prep_ct, "Swipe: ", swipe_ct, swipe_prep_ct)

        if swipe_prep_ct==2 and swipe_ct>0:
            # Detect Pinch
            if self.debug_mode:
                print("Detect Pinch")
            v1, v2 = list(swipes_prep.values())
            dex1, dey1 = v1
            dex2, dey2 = v2
            is_x_pinch = False
            is_y_pinch = False
            if abs(dex1)>self.pinch_x_min_dist and abs(dex2)>self.pinch_x_min_dist:
                if dex2*dex1<0:  # different sign
                    is_x_pinch=True
            if abs(dey1)>self.pinch_y_min_dist and abs(dey2)>self.pinch_y_min_dist:
                if dey2*dey1<0:  # different sign
                    is_y_pinch=True
            #TODO: Robustness improvement on distinguishing other similar gestures
            for i in swipes_prep:
                hist[i]["is_triggered"] = True
            if is_x_pinch or is_y_pinch:
                final_gesture = Gestures.PINCH
        elif swipe_ct == 1:
            if self.debug_mode:
                print("Detect 1 swip")
            itmp = list(swipes.keys())[0]
            vtmp = list(swipes.values())[0]
            dex, dey = vtmp
            hist[itmp]["is_triggered"] = True
            if abs(dex)<0.5*abs(dey) and abs(dey)>self.swipe_min_dist:  # up or down
                # up & down reversed due to cam angle
                if dey<0:
                    final_gesture = Gestures.SWIPE_DOWN
                else:
                    final_gesture = Gestures.SWIPE_UP
            elif abs(dey)<0.5*abs(dex) and abs(dex)>self.swipe_min_dist:  # left or right
                if dex<0:
                    final_gesture = Gestures.SWIPE_LEFT
                else:
                    final_gesture = Gestures.SWIPE_RIGHT
        elif hold_prep_ct==3 and hold_ct>0:
            if self.debug_mode:
                print("Detect 3 hold")
            for i in holds_prep:
                hist[i]["is_triggered"] = True
            final_gesture = Gestures.THREE_PRESS_HOLD
        elif hold_prep_ct==4 and hold_ct>0:
            if self.debug_mode:
                print("Detect 4 hold")
            for i in holds_prep:
                hist[i]["is_triggered"] = True
            final_gesture = Gestures.FOUR_PRESS_HOLD
        # else:
        #     if self.debug_mode:
        #         print("Hold: ",hold_ct,hold_prep_ct, "Swipe: ",swipe_ct,swipe_prep_ct)
        return final_gesture


    def process_single_gesture(self, history_ellipses):
        gesture = Single_Gestures.NO_GESTURE
        value = []
        first = history_ellipses[0]
        last = history_ellipses[-1]
        xf,yf = first[0]
        xl,yl = last[0]
        dex = xl-xf #delta_end_x
        dey = yl-yf
        if abs(dex)+abs(dey) < 20:
            gesture = Single_Gestures.PRESS_HOLD
        else:
            gesture = Single_Gestures.SWIPE
            value = [dex,dey]
        return gesture,value

class Ellipse_History:
    def __init__(self):
        self.history = {}
        self.id = 0
        self.not_detected_upper_bound = 3

    def add_one(self, ellipse):
        id = self.get_ellipse_id(ellipse)
        if id in self.history:
            self.history[id]["history"].append(ellipse)
            self.history[id]["not_detected_ct"] = 0
        else:
            self.history[id] = {"is_triggered":False,
                                "is_in_prep_state":False,
                                "is_in_detect_state":False,
                                "not_detected_ct":0,
                                "history":[ellipse],
                                "gesture":Single_Gestures.NO_GESTURE,
                                "value":[]}
        return id

    def add_many(self,list_of_ellipses):
        added_id = set()
        for ellipse in list_of_ellipses:
            added_id.add(self.add_one(ellipse))
        outdated_keys = []
        for i in self.history:
            if i not in added_id:
                self.history[i]["not_detected_ct"]+=1
            if self.history[i]["not_detected_ct"]>self.not_detected_upper_bound:
                outdated_keys.append(i)
        for i in outdated_keys:
            del self.history[i]

    def get_ellipse_id(self,ellipse_in,max_dist = 70):
        """
        Get ellipse id. If has existing ellipse in history that's close enough, return that id. If not, get a new id.
        :param ellipse_in: single ellipse
        :param max_dist: upper bound for two positions to be considered the same ellipse
        :return: ellipse id
        """
        xi,yi = ellipse_in[0]
        min_d = math.inf
        min_i = self.id
        for i,d in self.history.items():
            x,y = d["history"][-1][0]
            dist = abs(xi-x)+abs(yi-y)
            if dist < max_dist and dist < min_d:
                min_d = dist
                min_i = i
        if min_i == self.id:
            self.id+=1
        return min_i



