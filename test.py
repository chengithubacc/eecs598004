import cv2


camera = cv2.VideoCapture(1)
while True:
    ok, frame = camera.read()
    if ok:
        cv2.imshow("image", frame)
        cv2.moveWindow("image", 1, 1)
        cv2.waitKey(1)