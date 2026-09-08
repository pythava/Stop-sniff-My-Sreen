import pickle
import cv2
from insightface.app import FaceAnalysis


app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

cap = cv2.VideoCapture(0)
print("Look At me and press space")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Register Owner', frame)

    if cv2.waitKey(1) & 0xFF == ord(' '):
        faces = app.get(frame)
        if len(faces) == 0:
            print("face not detected. try again")
            continue

        owner_embedding = faces[0].embedding
        with open('owner.pkl', 'wb') as f:
            pickle.dump(owner_embedding, f)

        print("Successful to register root")
        break

cap.release()
cv2.destroyAllWindows()