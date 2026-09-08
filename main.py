import pickle
import cv2
import numpy as np
from plyer import notification
from insightface.app import FaceAnalysis
import time

def notice(title, message, app_name, timeout):
    notification.notify(
        title=title,
        message=message,
        app_name=app_name,
        timeout=timeout
    )

with open('owner.pkl', 'rb') as f:
    owner_embedding = pickle.load(f)

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(320, 320))

flag = 0
cap = cv2.VideoCapture(0)

THRESHOLD = 0.45
FLAG_time = 30
last_time = 0
return_time = 10

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    faces = app.get(frame)

    for face in faces:
        current_embedding = face.embedding

        similarity = np.dot(owner_embedding, current_embedding) / (
            np.linalg.norm(owner_embedding) * np.linalg.norm(current_embedding)
        )

        bbox = face.bbox.astype(int)
        if similarity >= THRESHOLD:
            text = f'Owner detected ({similarity:.2f})'
            color = (0, 255, 0)
        else:
            if last_time != 0:
                print(11)
                if int(time.time()) - last_time > return_time:
                    print(22)
                    flag = 0
                    last_time = int(time.time())
            else:
                print(44)
                last_time = int(time.time())
            text = f'Stranger Detected ({similarity:.2f})'
            if flag == 0:
                notice("Stranger Detected!!", "We detect Some Stranger on Your Cam", "Stop-sniff-My-Sreen", 5)

            flag += 1
            if flag >= FLAG_time:
                flag = 0
            
            print(flag)
            color = (0, 0, 255)

        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
        cv2.putText(
            frame,
            text,
            (bbox[0], bbox[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
        )
        
    cv2.imshow('face matcher', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()