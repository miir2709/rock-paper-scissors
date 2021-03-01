from flask import Flask
from flask import render_template, redirect, url_for, request, Response
import cv2

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        username = request.form['username']
        rounds=request.form['rounds']
        return redirect(url_for('PlayGame'))
    return render_template('home.html')



def gen_frames():  # generate frame by frame from camera
    camera = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            continue
        cv2.rectangle(frame, (50, 50), (400, 400), (255, 255, 255), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/play', methods=['GET', 'POST'])
def PlayGame():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == '__main__':
    app.run(debug=True)


# Home page:
# Rules, Start Game
# If Start Game toh ek form ayega. usme temp username, no of rounds input hoga. Uske badd play.html may videocapture hoga
####  def playgame may prediction aur scores update hoga. Computer keliye rock, paper, scissor ka image lagega
#### Jo score hoga wo play.html pe dikhana hai.