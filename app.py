from flask import Flask, render_template, Response, jsonify, redirect, url_for, request, flash, session
import cv2
import mediapipe as mp
import numpy as np
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

latest_status = {"label": "No Hands Detected", "handedness": "Unknown"}
camera_running = False
show_landmarks = True

# ✅ Predefined users (with password hashing)
users = {
    'Owaiz Ahmed': generate_password_hash('Owaiz@777')
}


# ------------------- HAND GESTURE FUNCTIONS -------------------
def is_finger_extended(tip, pip):
    return tip.y < pip.y


def is_finger_folded(tip, pip):
    return tip.y > pip.y


def classify_gesture(landmarks):
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    index_tip = landmarks[8]
    index_pip = landmarks[6]
    middle_tip = landmarks[12]
    middle_pip = landmarks[10]
    ring_tip = landmarks[16]
    ring_pip = landmarks[14]
    pinky_tip = landmarks[20]
    pinky_pip = landmarks[18]
    wrist = landmarks[0]

    index_ext = is_finger_extended(index_tip, index_pip)
    middle_ext = is_finger_extended(middle_tip, middle_pip)
    ring_ext = is_finger_extended(ring_tip, ring_pip)
    pinky_ext = is_finger_extended(pinky_tip, pinky_pip)

    index_fld = is_finger_folded(index_tip, index_pip)
    middle_fld = is_finger_folded(middle_tip, middle_pip)
    ring_fld = is_finger_folded(ring_tip, ring_pip)
    pinky_fld = is_finger_folded(pinky_tip, pinky_pip)

    thumb_up = thumb_tip.y < wrist.y and abs(thumb_tip.x - wrist.x) < 0.2
    thumb_index_dist = np.linalg.norm(
        np.array([thumb_tip.x, thumb_tip.y]) - np.array([index_tip.x, index_tip.y])
    )

    if all([index_ext, middle_ext, ring_ext, pinky_ext]):
        return "Hi/Hello/Bye 👋"

    if all([index_fld, middle_fld, ring_fld, pinky_fld]):
        return "Fist 👊"

    if thumb_tip.y < thumb_ip.y and pinky_ext and all([middle_fld, ring_fld, index_fld]):
        return "Call Me 📞"

    if thumb_tip.y < thumb_ip.y and index_ext and pinky_ext and middle_fld and ring_fld:
        return "I Love You ❤️"

    if index_ext and pinky_ext and all([middle_fld, ring_fld]):
        return "Rock On 🤘"

    if index_ext and middle_ext and all([ring_fld, pinky_fld]):
        return "Peace ✌️"

    if index_ext and all([middle_fld, ring_fld, pinky_fld]) and thumb_up:
        return "Point Up ☝️"

    if thumb_index_dist < 0.05:
        return "OK 👌"

    return "Unknown 🤷‍♂️"


# ------------------- CAMERA FUNCTION -------------------
def gen():
    global latest_status, camera_running, show_landmarks
    cap = cv2.VideoCapture(0)
    while camera_running:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                x_coords = [lm.x for lm in hand_landmarks.landmark]
                y_coords = [lm.y for lm in hand_landmarks.landmark]
                x_min = int(min(x_coords) * w) - 20
                y_min = int(min(y_coords) * h) - 20
                x_max = int(max(x_coords) * w) + 20
                y_max = int(max(y_coords) * h) + 20
                x_min, y_min = max(0, x_min), max(0, y_min)
                x_max, y_max = min(w, x_max), min(h, y_max)

                gesture = classify_gesture(hand_landmarks.landmark)
                hand_label = handedness.classification[0].label

                latest_status["label"] = gesture
                latest_status["handedness"] = hand_label

                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)
                cv2.putText(frame, gesture, (x_min + 10, y_min - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                if show_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=3),
                        mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
                    )
        else:
            latest_status["label"] = "No Hands Detected"
            latest_status["handedness"] = "Unknown"

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()


# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if username not in users:
            flash("Username does not exist!", "danger")
            return render_template('login.html')

        if not check_password_hash(users[username], password):
            flash("Incorrect password!", "danger")
            return render_template('login.html')

        session['user'] = username
        flash("Logged out successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            flash("Please enter username and password", "danger")
            return render_template('register.html')

        if username in users:
            flash("Username already exists", "danger")
            return render_template('register.html')

        if len(password) < 7 or \
           not re.search(r"[A-Z]", password) or \
           not re.search(r"[a-z]", password) or \
           not re.search(r"[0-9]", password) or \
           not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must contain uppercase, lowercase, number & symbol", "danger")
            return render_template('register.html')

        users[username] = generate_password_hash(password)
        flash("Registered successfully. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    username = session['user']
    return render_template('dashboard.html', username=username)


@app.route('/index')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    username = session['user']
    return render_template('index.html', username=username)


@app.route('/video_feed')
def video_feed():
    if 'user' not in session:
        return jsonify({"error": "not_logged_in"})
    if not camera_running:
        return jsonify({"error": "camera_not_running"})
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/gesture')
def gesture():
    if 'user' not in session:
        return jsonify({"label": "No Hands Detected", "handedness": "Unknown"})
    return jsonify(latest_status)


@app.route('/start_camera', methods=['POST'])
def start_camera():
    global camera_running
    camera_running = True
    return jsonify({"status": "Camera started"})


@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global camera_running
    camera_running = False
    return jsonify({"status": "Camera stopped"})


@app.route('/toggle_landmarks', methods=['POST'])
def toggle_landmarks():
    global show_landmarks
    show_landmarks = not show_landmarks
    return jsonify({"show_landmarks": show_landmarks})


@app.route('/get_landmark_status')
def get_landmark_status():
    return jsonify({"show_landmarks": show_landmarks})


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/learn')
def learn():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('learn.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ------------------- MAIN -------------------
if __name__ == '__main__':
    os.makedirs("logs", exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
