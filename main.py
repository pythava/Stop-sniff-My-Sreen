import pickle
import cv2
import numpy as np
from plyer import notification
from insightface.app import FaceAnalysis
import time
from datetime import datetime
from collections import deque

def notice(title, message, app_name, timeout):
    notification.notify(
        title=title,
        message=message,
        app_name=app_name,
        timeout=timeout
    )

# 이거 로그기능인데 언젠가 사용하기
def logs(user, message, start_time):
    with open(f'screen{now.date()}.log', 'a', encoding='utf-8') as log_file:
        text = f"[{user}]\t"
        text += message + "\t"
        text += str(start_time) 
        text += " ~ "
        log_file.write(text)

# 로그에서 마지막으로 남은 로그 유저 가져오는 로직 
def bring_auth():
    try:
        with open(f"screen{now.date()}.log", "r", encoding="utf-8") as log_file:
            last_line = deque(log_file, maxlen=1)
            line = last_line[0] if last_line else ""    

        if line == "":
            return ""
        else:
            auth = line[1:]
            idx = auth.find("]")
            auth = auth[:idx]
            return auth
    except FileNotFoundError as e:
        print(f"[Error] file open error : {e}")
        
    
try:
    with open('owner.pkl', 'rb') as f:
        owner_embedding = pickle.load(f)
except FileNotFoundError as e:
    print(f"[Error] file open error : {e}")
    exit()

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(320, 320))

flag = 0
detector = ""
detection_time = 0
cap = cv2.VideoCapture(0)

THRESHOLD = 0.45
FLAG_time = 30
last_time = 0
return_time = 10

now = time


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
            
            # 여기서 마지막 로그로 남은 유저가 Owner라면 그대로 카운트 하고 아니면 현재 시각을 기록하고 Owner로 기록 시작하기
            if bring_auth() != "Owner":
                with open(f'screen{now.date()}.log', 'a', encoding='utf-8') as log_file:
                    #log_file.write(str(time.time()))
                    log_file.write("\n")
                    logs("Owner", "Owner detectecd", time.time())
                    print("not Owner1111111111111")
                    
            color = (0, 255, 0)
            f.write
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
            
            if bring_auth() != "Stranger":
                with open(f'screen{now.date()}.log', 'a', encoding='utf-8') as log_file:
                    #log_file.write(str(time.time()))
                    log_file.write("\n")
                    logs("Stranger", "Stranger detectecd", time.time())
                    print("not Stranger2222222222222222222222")        
            
            
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