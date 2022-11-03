import cv2

a = cv2.VideoCapture('test_media/a.mp4')
while True:
    success, frame = a.read()
    print(type(frame))
    break