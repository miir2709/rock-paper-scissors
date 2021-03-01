import cv2
import numpy as np 
import os
import time
from keras.models import load_model

label_names = ['paper', 'rock', 'scissors']
model = load_model('vggmodel_28_02_final.h5')

cap = cv2.VideoCapture(0)
start = False
#No of rounds
count = 5
no = 0
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    cv2.rectangle(frame, (50, 50), (400, 400), (255, 255, 255), 2)

    if start:
        img = frame[50:400, 50:400]
        img = np.expand_dims(img, axis=0)
        pred = np.argmax(model.predict(img))
        label = label_names[pred]
        start = False
        no += 1
        time.sleep(1)
    try:
        cv2.putText(frame, f"User Action Round {no} : {label}", (5,50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    except:
        pass
    cv2.imshow("Rock Paper Scissor Game", frame)

    k = cv2.waitKey(10)
    if k == ord('a'):
        start = True
    if k == ord('q'):
        break

    if count == no:
        break

cap.release()
cv2.destroyAllWindows()