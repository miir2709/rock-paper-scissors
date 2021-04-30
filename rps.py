from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime
from PyQt5.QtCore import *
import sys
import cv2
import numpy as np
from keras.models import load_model
import random
import imutils
import time


def winnerOfOneRound(move1, move2, username):
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        if move2 == "scissors":
            return username
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return username
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return username
        if move2 == "rock":
            return "Computer"

def Start(model, username, num_rounds):
    label_names = ['paper', 'rock', 'scissors']
    model = load_model('models/vggmodel_28_02_final.h5')
    comp_images = ['rock', 'paper', 'scissors']
    cap = cv2.VideoCapture(0)
    start = False
    #No of rounds
    count = num_rounds
    no = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    countScoreOfUser = 0
    countScoreofComputer = 0
    countTie = 0
    duration = 3
    x = 0
    start_time = None
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (900, 600))
        cv2.putText(frame, f"Press 'a' to click the image. Press 'q' to quit the game", (50,450), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
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
            winner = winnerOfOneRound(label, comp_move, username)

            if winner == username:
                countScoreOfUser += 1
            elif winner == 'Computer':
                countScoreofComputer += 1
            else:
                countTie += 1
            time.sleep(1)
        try:
            #icon = cv2.resize(icon, (400, 400))
            #frame[100:500, 800:1200] = icon
            cv2.putText(frame, f"{username} Action Round {no} : {label}", (5,50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Winner Of Round {no} : {winner}", (400,50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, f"User Score: {countScoreOfUser} | Computer Score: {countScoreofComputer}", (5,550), font, 0.5, (0, 255, 255), 2, cv2.LINE_AA)

            icon = cv2.resize(icon, (350, 350))
            frame[50:400, 450:800] = icon
            start_time = datatime.now()
        except:
            pass
        cv2.imshow("Rock Paper Scissor Game", frame)

        k = cv2.waitKey(10)
        if k == ord('a'):
            start = True
            x = 1
        if k == ord('q'):
            break

        if count == no:
            break

    cap.release()
    cv2.destroyAllWindows()
    return (countScoreOfUser, countScoreofComputer)

class Ui_Dialog(object):

    def StartGame(self, num_rounds, username, Dialog):
        flag = 0
        try:
            num_rounds = int(num_rounds.toPlainText())
            if num_rounds <= 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Incorrect Number of rounds!")
                msg.setWindowTitle("Error")
                msg.exec_()
                flag = 1
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error in Number of rounds!")
            msg.setWindowTitle("Error")
            msg.exec_()
            flag = 1
        if flag == 0:
            model = load_model('models/vggmodel_28_02_final.h5')
            MainWindow.hide()
            Dialog.hide()
            username = username.toPlainText()
            
            user, computer = Start(model, username, num_rounds)
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_ResultWindow()
            self.ui.setupUi(self.window, user, computer, username)
            MainWindow.show()
            self.window.show()    
            
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(237, 241)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 190, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(73, 140, 101, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_2.setGeometry(QtCore.QRect(73, 80, 101, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 30, 110, 60))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 100, 100, 60))
        self.label_2.setObjectName("label_2")
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(lambda: self.StartGame(self.textEdit, self.textEdit_2, Dialog))
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Username"))
        self.label_2.setText(_translate("Dialog", "Number of Rounds"))



class Ui_ResultWindow(object):
    def setupUi(self, ResultWindow, user, computer, username):
        ResultWindow.setObjectName("ResultWindow")
        ResultWindow.resize(387, 169)
        self.centralwidget = QtWidgets.QWidget(ResultWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 40, 81, 41))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 40, 71, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(100, 80, 120, 41))
        self.label_3.setObjectName("label_3")
        ResultWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ResultWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 387, 21))
        self.menubar.setObjectName("menubar")
        ResultWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ResultWindow)
        self.statusbar.setObjectName("statusbar")
        ResultWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ResultWindow, user, computer, username)
        QtCore.QMetaObject.connectSlotsByName(ResultWindow)

    def retranslateUi(self, ResultWindow, user, computer, username):
        _translate = QtCore.QCoreApplication.translate
        ResultWindow.setWindowTitle(_translate("ResultWindow", "ResultWindow"))
        self.label.setText(_translate("ResultWindow", f"{username}: {user}"))
        self.label_2.setText(_translate("ResultWindow", f"Computer: {computer}"))
        if user == computer:
            res = 'Tie'
        elif user > computer:
            res = username
        else:
            res = 'Computer'
        self.label_3.setText(_translate("ResultWindow", f"Result: {res}"))


class Ui_MainWindow(object):

    def OpenRules(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_RuleWindow()
        self.ui.setupUi(self.window)
        MainWindow.close()
        self.window.show()

    def InputWindow(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        MainWindow.hide()
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Rock Paper Scissor - Home")
        MainWindow.setFixedSize(386, 269)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(-10, -10, 461, 331))
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 20, 261, 31))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 180, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 180, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 386, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"images.jpg\" /></p></body></html>"))
        self.label.setText(_translate("MainWindow", "<html><head><head/><body><p><span style=\" font-size:16pt; font-weight:600; color:#ececec;\">Rock Paper Scissors</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Rules"))
        self.pushButton.clicked.connect(self.OpenRules)
        self.pushButton_2.setText(_translate("MainWindow", "Start"))
        self.pushButton_2.clicked.connect(self.InputWindow)


class Ui_RuleWindow(object):

    def OpenMain(self, RuleWindow):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        RuleWindow.close()
        self.window.show()

    def InputWindow(self, RuleWindow):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        RuleWindow.close()
        self.window.show()

    def setupUi(self, RuleWindow):
        RuleWindow.setObjectName("Rock Paper Scissor - Rules")
        RuleWindow.setFixedSize(885, 384)
        self.centralwidget = QtWidgets.QWidget(RuleWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(-390, -60, 1281, 631))
        self.textBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser.setObjectName("textBrowser")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(490, 50, 401, 241))
        self.label.setObjectName("label")
        RuleWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RuleWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 885, 21))
        self.menubar.setObjectName("menubar")
        RuleWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RuleWindow)
        self.statusbar.setObjectName("statusbar")
        RuleWindow.setStatusBar(self.statusbar)
        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(200, 30, 75, 23))
        self.pushButton_1.setObjectName("pushButton_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 30, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.retranslateUi(RuleWindow)
        QtCore.QMetaObject.connectSlotsByName(RuleWindow)

    def retranslateUi(self, RuleWindow):
        _translate = QtCore.QCoreApplication.translate
        RuleWindow.setWindowTitle(_translate("RuleWindow", "RuleWindow"))
        self.textBrowser.setHtml(_translate("RuleWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"wp8121942.png\" /></p></body></html>"))
        self.label.setText(_translate("RuleWindow", "<html><head/>\n"
"<body><ul><li><p><span style=\" font-size:14pt;\">Allow use of webcam to collect images</span></p></li><li><p><span style=\" font-size:14pt;\">Use three actions : rock, paper, scissors</span></p></li><li><p><span style=\" font-size:14pt;\">Use a plain background</span></p></li><li><p><span style=\" font-size:14pt;\">Rock crushes Scissors</span></p></li><li><p><span style=\" font-size:14pt;\">Scissors cuts Paper</span></p></li><li><p><span style=\" font-size:14pt;\">Paper covers Rock</span></p></li></ul></body></html>"))
        self.pushButton_2.setText(_translate("RuleWindow", "Main"))
        self.pushButton_2.clicked.connect(lambda: self.OpenMain(RuleWindow))
        self.pushButton_1.setText(_translate('RuleWindow', 'Start'))
        self.pushButton_1.clicked.connect(lambda: self.InputWindow(RuleWindow))
        #self.pushButton_2.clicked.connect(self.StartGame)




if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())