import cv2
import numpy as np
import os
import time

label_names = ['scissors']

for label_name in label_names:
  IMG_SAVE_PATH = 'test_images2'
  IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, label_name)
  try:
    os.mkdir(IMG_SAVE_PATH)
  except FileExistsError:
    pass
  try:
    os.mkdir(IMG_CLASS_PATH)
  except FileExistsError:
    pass

  cap = cv2.VideoCapture(0)
  start = False
  count = 300
  while True:
    ret, frame = cap.read()
    if not ret:
      continue

    if count == 400:
      break

    cv2.rectangle(frame, (50, 50), (400, 400), (255, 255, 255), 2)

    if start:
      roi = frame[50:400, 50:400]
      save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(count+1))
      cv2.imwrite(save_path, roi)
      count += 1

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f"Collecting {count}", (5,50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Collecting images", frame)
    time.sleep(0.2)
    k = cv2.waitKey(10)
    if k == ord('a'):
      start = not start
    if k == ord('q'):
      break
  print(f"\n{count} images saved to {IMG_CLASS_PATH}")
  cap.release()
  cv2.destroyAllWindows()