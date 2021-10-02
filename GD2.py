import math
from enum import Enum
class Gestures(Enum):
    NO_GESTURE=0
    PRESS_HOLD=1
    SWIPE_UP=2
    SWIPE_DOWN=3
    SWIPE_LEFT=4
    SWIPE_RIGHT=5

class Single_Gestures(Enum):
    NO_GESTURE=0
    PRESS_HOLD=1
    SWIPE=2

class GD2:
    def __init__(self, min_wait_frame = 5):
        self.history = Ellipse_History()
        self.min_wait_frame = min_wait_frame

    def print_single_gestures(self):
        printed = False
        for i,d in self.history.history.items():
            printed = True
            print(i,": ",d["gesture"],end=" ")
        if printed:
            print()

    def add_ellipses(self,list_of_ellipses):
        self.history.add_many(list_of_ellipses)

    def detect_gesture(self):
        hist = self.history.history
        for i,d in hist.items():
            if not d["is_triggered"] and len(d["history"])>self.min_wait_frame:
                single_hist = d["history"]
                gesture, value = self.process_single_gesture(single_hist)
                hist[i]["gesture"] = gesture
                hist[i]["value"] = value
        gesture = self.process_gesture(hist)
        #self.print_single_gestures()
        return gesture


    def process_gesture(self,hist):
        final_gesture = Gestures.NO_GESTURE
        hold_ct = 0
        swipe_ct = 0
        swipes = {}
        for i,d in hist.items():
            if not d["is_triggered"]:
                if d["gesture"] == Single_Gestures.PRESS_HOLD:
                    hold_ct+=1
                elif d["gesture"] == Single_Gestures.SWIPE:
                    swipe_ct+=1
                    swipes[i] = d["value"]
        if swipe_ct == 1:
            itmp = list(swipes.keys())[0]
            vtmp = list(swipes.values())[0]
            dex, dey = vtmp
            hist[itmp]["is_triggered"] = True
            if abs(dex)<0.5*abs(dey):  # up or down
                if dey<0:
                    final_gesture = Gestures.SWIPE_UP
                else:
                    final_gesture = Gestures.SWIPE_DOWN
            elif abs(dey)<0.5*abs(dex):  # left or right
                if dex<0:
                    final_gesture = Gestures.SWIPE_LEFT
                else:
                    final_gesture = Gestures.SWIPE_RIGHT

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
        self.not_detected_upper_bound = 5

    def add_one(self, ellipse):
        id = self.get_ellipse_id(ellipse)
        if id in self.history:
            self.history[id]["history"].append(ellipse)
            self.history[id]["not_detected_ct"] = 0
        else:
            self.history[id] = {"is_triggered":False,
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

    def get_ellipse_id(self,ellipse_in,max_dist = 50):
        """
        Get ellipse id. If has existing ellipse in history that's close enough, return that id. If not, get a new id.
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



def process_gesture(pos_history:dict,buffer_size):
    pos_dict = {}
    for i,j in pos_history.items():
        if j[-1] is None:
            continue
        valid_bboxes = []
        consec_none_ct = 0
        for ii in range(1, buffer_size+1):
            if j[-ii] is None or j[-ii] is [0,0,0,0]:
                consec_none_ct+=1
            else:
                valid_bboxes.append(j[-ii])
                consec_none_ct = 0
            if consec_none_ct>5:
                break
        # if len(valid_bboxes)>0:
        #     print(len(valid_bboxes))
        if len(valid_bboxes)>20:
            xs,ys,ws,hs = valid_bboxes[0]
            xe,ye,we,he = valid_bboxes[-1]
            dx = xe-xs
            dy = ye-ys
            if dx<10 and dy<10:
                continue
            dyd = 1 if dy==0 else dy
            xyr = dx/dyd
            if not 0.3<xyr<3:
                if abs(dx)>abs(dy):
                    if dx<0:
                        pos_dict[i] = "left"
                    else:
                        pos_dict[i] = "right"
                else:
                    if dy>0:
                        pos_dict[i] = "up"
                    else:
                        pos_dict[i] = "down"
            #print(valid_bboxes)
    return pos_dict

