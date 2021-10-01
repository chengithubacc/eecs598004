import cv2


class Touch_Detector:
    def __init__(self, grayscale_threshold=200, width_height_ratio_threshold = 0.3, min_touch_area=500, max_touch_area=7000):
        """
        Initialization
        :param grayscale_threshold: lower threshold for filtering bright pixels
        """
        self.grayscale_threshold = grayscale_threshold
        self.width_height_ratio_threshold = width_height_ratio_threshold
        self.min_touch_area = min_touch_area
        self.max_touch_area = max_touch_area

    def is_ellipse_valid(self,ellipse):
        # check ratio
        x,y = ellipse[0]
        w,h = ellipse[1]
        r = ellipse[2]
        return w>self.width_height_ratio_threshold*h and h>self.width_height_ratio_threshold*w

    def get_touch_ellipses(self, gray_frame):
        """
        Get touch ellipse and location for a given grayscale frame
        :param gray_frame: input grayscale frame
        :return: a list of ellipses
        """
        threshold_image = cv2.inRange(gray_frame, self.grayscale_threshold, 255)
        contours, hierarchy = cv2.findContours(image=threshold_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        possible_ellipses = []
        for cnt in contours:
            if self.max_touch_area>cv2.contourArea(cnt)>self.min_touch_area:
                ellipse = cv2.fitEllipse(cnt)
                if self.is_ellipse_valid(ellipse):
                    possible_ellipses.append(ellipse)
        return possible_ellipses

    def visualize(self, ellipses, image):
        """
        visualize touches and show coordinates
        :param ellipses: a list of valid ellipses
        :param image: RGB image for visualization
        :return: modified RGB image
        """
        for e in ellipses:
            x, y = e[0]
            w, h = e[1]
            r = e[2]
            cv2.ellipse(image, e, (0, 0, 255), 5)
            text_string = 'x:'+str(round(x, 2))+' y:'+str(round(y, 2))+'\n'+'w:'+str(round(w, 2))+' h:'+str(round(h, 2))
            cv2.putText(image, text_string, (int(x+50), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),1)
        return image
