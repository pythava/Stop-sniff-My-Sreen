import cv2
import mediapipe as mp
from plyer import notification

FLAG = 0
MAX_FLAG_NUM = 400


def notice(title, message, app_name, timeout):
    notification.notify(
        title=title,
        message=message,
        app_name=app_name,
        timeout=timeout
    )

# MediaPipe 얼굴 감지 도구 불러오기
mp_face_detection = mp.solutions.face_detection

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("can't open the webcam. pls check")
    exit()

print("AI detection active (Console mode). press 'q' to exit")

with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5
) as face_detection:

    while True:
        ret, frame = cap.read()

        if not ret:
            print("failed to read frame")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_detection.process(rgb_frame)

        if results.detections:
            if FLAG == 1:
                notice("Face Detected!!!", "we Detected face on your cam", "Stop-Sniff-My-Screen", 2)
            FLAG += 1
            if FLAG >= MAX_FLAG_NUM:
                FLAG = 0
        else:
            FLAG = 0

            
        cv2.imshow("Webcam Monitor", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()