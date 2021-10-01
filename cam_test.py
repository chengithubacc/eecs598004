import cv2
camera_port = 1
camera = cv2.VideoCapture(camera_port)
while True:
    ret, frame = camera.read()
    cv2.imshow('l1',frame[:,:,0])
    cv2.imshow('l2',frame[:,:,1])
    cv2.imshow('l3',frame[:,:,2])
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray',img_gray)
    threshold_image = cv2.inRange(img_gray, 200, 255)
    contours, hierarchy = cv2.findContours(image=threshold_image, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    image_copy = threshold_image.copy()
    image_copy = cv2.cvtColor(image_copy, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                     lineType=cv2.LINE_AA)
    possible_ellipse = []

    def is_ellipse_valid(ellipse):
        # check ratio
        x,y = ellipse[0]
        w,h = ellipse[1]
        r = ellipse[2]
        return w>0.3*h and h>0.3*w

    for cnt in contours:
        if cv2.contourArea(cnt)>500:
            ellipse = cv2.fitEllipse(cnt)
            if is_ellipse_valid(ellipse):
                print(ellipse)
                print("-------")
                cv2.ellipse(image_copy, ellipse, (255, 0, 255), 2)
                possible_ellipse.append(ellipse)

    cv2.imshow('threshold',image_copy)
    cv2.waitKey(1)