import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
#picam2.preview_configuration.main.size = (1280, 720)
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

im = picam2.capture_array()
print(im)
print(type(im))
cv2.imshow("Camera", im)
cv2.imwrite("output.jpg", im)
with open("output.jpg", 'rb') as im:
    image_bytes = im.read()

print(image_bytes)