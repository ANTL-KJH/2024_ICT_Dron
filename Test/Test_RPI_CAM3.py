import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "BGR888"  # BGR 형식으로 변경
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

while True:
    im = picam2.capture_array()

    # OpenCV imshow를 사용하여 이미지 표시
    cv2.imshow("Camera", im)

    # 키 입력을 기다리고 'q'가 입력되면 루프를 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# OpenCV 창 닫기 및 Picamera2 종료
cv2.destroyAllWindows()
picam2.stop()
