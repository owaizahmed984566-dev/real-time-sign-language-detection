# 🤟 Real-Time Sign Language Detection

> A web-based computer vision application that detects predefined hand gestures in real time using OpenCV and MediaPipe, with an interactive Flask interface for gesture interpretation and learning.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red?logo=opencv)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)
[![NumPy](https://img.shields.io/badge/NumPy-Computing-013243?logo=numpy)](https://numpy.org/)

---

## 📌 Overview

**Real-Time Sign Language Detection** is a web-based application designed to recognize predefined hand gestures through a webcam and present their corresponding meanings through an interactive user interface.

The application combines **Flask, OpenCV, MediaPipe Hands, NumPy, HTML, CSS, and JavaScript** to create a real-time gesture recognition system.

The webcam captures live frames, MediaPipe detects hand landmarks, and the application analyzes landmark positions and finger states to classify supported gestures.

The system also provides user authentication, a dashboard, Learn Mode, gesture information, camera controls, and optional visual/voice feedback.

---

## 🎯 Project Objectives

- Develop a real-time hand gesture recognition system.
- Detect hand landmarks from webcam input.
- Classify a predefined set of gestures.
- Provide an interactive interface for gesture interpretation.
- Provide a Learn Mode for understanding supported gestures.
- Provide visual and optional audio feedback.
- Create an accessible foundation for future sign-language translation systems.

---

## ✨ Key Features

- 🎥 Real-time webcam-based gesture detection
- ✋ 21-point hand landmark detection using MediaPipe Hands
- 🧠 Landmark-based rule classification
- 🔐 User registration and login
- 🔑 Password hashing using Werkzeug
- 📊 Interactive dashboard
- 📚 Learn Mode
- 🗣️ Gesture meaning and voice feedback
- 🖐️ Show/Hide hand landmarks
- ▶️ Start/Stop camera controls
- 👋 Gesture and handedness information
- 🎨 Interactive web interface
- 📑 Gesture status/history interface

---

## 🤟 Supported Gestures

| Gesture | Meaning |
|---|---|
| 👋 Hi / Hello / Bye | Greeting |
| 👊 Fist | Strong / Stop |
| 📞 Call Me | Phone call |
| ❤️ I Love You | Expression of love |
| 🤘 Rock On | Rock music / excitement |
| ✌️ Peace | Victory / peace |
| ☝️ Point Up | Pointing upwards |
| 👌 OK | Everything is fine |

---

## 🧠 How the System Works

```text
                Webcam
                   │
                   ▼
             OpenCV Capture
                   │
                   ▼
           Frame Preprocessing
                   │
                   ▼
           MediaPipe Hands
                   │
                   ▼
        21 Hand Landmark Points
                   │
                   ▼
      Finger Position Analysis
                   │
                   ▼
       Gesture Classification
                   │
                   ▼
        Detected Gesture Label
                   │
          ┌────────┴────────┐
          ▼                 ▼
      Web Interface      Voice/Meaning
```

---

## 🔍 Gesture Detection Method

The current implementation uses **hand landmarks and rule-based classification**.

For each detected hand, the application evaluates landmark positions and finger states such as:

- Finger extension
- Finger folding
- Thumb position
- Thumb-index distance
- Relative landmark positions

These conditions are combined to classify the predefined gestures.

The system currently supports a single detected hand at a time and uses MediaPipe's handedness information to identify the detected hand.

---

## 🏗️ Application Architecture

```text
┌─────────────────────────────────────┐
│           User / Browser            │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          Flask Web Application       │
│                                     │
│  Login │ Register │ Dashboard       │
│  Learn │ Detection │ About          │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          Camera Processing           │
│                                     │
│              OpenCV                 │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          Hand Detection              │
│                                     │
│          MediaPipe Hands             │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│       Landmark-Based Classifier      │
│                                     │
│ Finger States + Distances + Rules   │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│       Gesture Result / Meaning       │
└─────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

- **Python**
- **Flask**

### Computer Vision

- **OpenCV**
- **MediaPipe Hands**
- **NumPy**

### Frontend

- **HTML5**
- **CSS3**
- **JavaScript**

### Security

- **Werkzeug Password Hashing**
- **Flask Sessions**

---

## 📂 Project Structure

```text
real-time-sign-language-detection/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── index.html
│   ├── learn.html
│   └── about.html
│
├── static/
│   ├── css/
│   ├── js/
│   ├── pic/
│   └── videos/
│
├── presentation/
│   └── sign-language-presentation.html
│
└── screenshots/
    ├── login.png
    ├── dashboard.png
    ├── detection.png
    └── learn-mode.png
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/real-time-sign-language-detection.git
```

### 2. Navigate to the Project

```bash
cd real-time-sign-language-detection
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

Then open the application in your browser:

```text
http://127.0.0.1:5000
```

The application starts the Flask server on port `5000`.

---

## 👤 Application Flow

```text
             Register
                │
                ▼
              Login
                │
                ▼
            Dashboard
                │
        ┌───────┴────────┐
        ▼                ▼
    Learn Mode      Interpret Mode
                         │
                         ▼
                    Start Camera
                         │
                         ▼
                  Detect Gesture
                         │
                         ▼
                Display Result
```

---

## 🔐 Authentication

The application provides:

- User registration
- Login validation
- Password hashing
- Session-based authentication
- Logout functionality
- Protected application routes

Passwords are hashed using Werkzeug before being stored in the application's user structure.

> **Note:** The current prototype uses in-memory user storage. Registered users are therefore not persistent after the application process is restarted.

---

## 📡 Flask Routes

The application provides routes for:

| Route | Purpose |
|---|---|
| `/` | Redirects to login |
| `/login` | User login |
| `/register` | User registration |
| `/dashboard` | User dashboard |
| `/index` | Gesture detection interface |
| `/video_feed` | Live camera stream |
| `/gesture` | Current gesture information |
| `/start_camera` | Start camera |
| `/stop_camera` | Stop camera |
| `/toggle_landmarks` | Toggle hand landmarks |
| `/get_landmark_status` | Get landmark visibility status |
| `/learn` | Learn Mode |
| `/about` | About page |
| `/logout` | Logout |

---

## 📸 Screenshots

### Login

![Login](screenshots/login.png)

### Dashboard

![Dashboard](screenshots/dashboard.png)

### Real-Time Detection

![Detection](screenshots/detection.png)

### Learn Mode

![Learn Mode](screenshots/learn-mode.png)

> Screenshots will be added as the project repository is finalized.

---

## 🎥 Project Presentation

A complete project presentation is included in the `presentation/` directory.

The presentation covers:

- Problem Statement
- Objectives
- Related Work
- System Architecture
- Hand Landmarks
- Features
- Classification Pipeline
- Dataset
- Implementation
- Backend
- Frontend & UX
- Demo Flow
- Results
- Applications
- Future Work
- Conclusion

---

## 💡 Use Cases

The system can serve as a foundation for:

- Sign language learning applications
- Educational accessibility tools
- Gesture-based interfaces
- Assistive communication systems
- Interactive demonstrations
- Future real-time sign language translation systems

---

## ⚠️ Current Limitations

- The current system supports a predefined gesture vocabulary.
- Classification depends on landmark positions and predefined rules.
- Recognition can be affected by lighting, camera quality, hand orientation, and background conditions.
- The current prototype supports one hand at a time.
- User accounts are stored in memory and are not persistent after application restart.
- Continuous sentence-level sign language translation is not currently implemented.
- The current implementation is a prototype and requires further testing for real-world deployment.

---

## 🚀 Future Improvements

- Expand the gesture vocabulary.
- Implement continuous sign/sentence recognition.
- Add persistent database-backed user authentication.
- Improve recognition under different lighting and backgrounds.
- Support multiple hands.
- Improve gesture classification using trained machine-learning models.
- Add multilingual gesture meanings.
- Develop mobile and edge-device versions.
- Improve personalization and accessibility.
- Add more advanced evaluation and real-world testing.

---

## 🔒 Security & Repository Notes

The following local files/directories should not be committed to the public repository:

```text
users.db
instance/
logs/
.env
venv/
```

Sensitive credentials and configuration values should never be committed to GitHub.

---

## 🎓 Academic Project

This project was developed as a **Final Year Project** in Computer Science.

### Project Title

**Real-Time Sign Language Detection**

### Team

- Owaiz Ahmed
- Sahil Ahamed
- Syed Moaz
- Umer Khan

### Institution

**Ghousia College of Engineering**

---

## 📌 Project Status

**Status:** Completed Academic Prototype

The project provides a working foundation for real-time predefined hand gesture recognition through a web-based interface.

---

## 🤝 Contributing

This repository represents an academic project.

Suggestions, improvements, and technical contributions are welcome.

---

## 📄 License

This project was developed for academic and educational purposes.

---

## ⭐ Acknowledgements

- OpenCV
- MediaPipe
- Flask
- NumPy
- Werkzeug

---

## 👨‍💻 Author

**Owaiz Ahmed**

Computer Science Engineering  
Java Backend Developer | Software Development

---

⭐ If you find this project interesting, consider giving the repository a star!