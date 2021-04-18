import cv2
from keras.models import load_model
import os
import numpy as np
import time
import random
import imutils


def winnerOfOneRound(move1, move2):
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        if move2 == "scissors":
            return "User"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "User"
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return "User"
        if move2 == "rock":
            return "Computer"


def Start():
    label_names = ['paper', 'rock', 'scissors']
    model = load_model('models/vggmodel_28_02_final.h5')
    comp_images = ['rock', 'paper', 'scissors']
    cap = cv2.VideoCapture(0)
    start = False
    #No of rounds
    count = 5
    no = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    countScoreOfUser = 0
    countScoreofComputer = 0
    countTie = 0
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (900, 600))

        if not ret:
            continue
        cv2.rectangle(frame, (50, 50), (400, 400), (255, 255, 255), 2)
        cv2.rectangle(frame, (450, 50), (800, 400), (255, 255, 255), 2)
        if start:
            img = frame[50:400, 50:400]
            img = np.expand_dims(img, axis=0)
            pred = np.argmax(model.predict(img))
            label = label_names[pred]
            start = False
            idx = random.randint(0, 2)
            comp_move = comp_images[idx]
            icon = cv2.imread(comp_move + '.png')
            no += 1
            winner = winnerOfOneRound(label, comp_move)

            if winner == 'User':
                countScoreOfUser += 1
            elif winner == 'Computer':
                 countScoreofComputer += 1
            else:
                countTie += 1
            time.sleep(1)
        try:
            #icon = cv2.resize(icon, (400, 400))
            #frame[100:500, 800:1200] = icon
            cv2.putText(frame, f"User Action Round {no} : {label}", (5,50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Winner Of Round {no} : {winner}", (400,50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"User Score: {countScoreOfUser} | Computer Score: {countScoreofComputer}", (5,550), font, 0.5, (0, 255, 255), 2, cv2.LINE_AA)

            icon = cv2.resize(icon, (350, 350))
            frame[50:400, 450:800] = icon
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
    return (countScoreOfUser, countScoreofComputer)