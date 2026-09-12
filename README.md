# 🎛️ Virtual Knob

A webcam-based hand gesture controller for controlling system media and volume without touching the keyboard or mouse.

Built with **Python, OpenCV, MediaPipe, PyAutoGUI and Windows audio controls**.

## ✨ Features

* 🖐️ Webcam-based hand tracking
* 🎯 Gesture-based activation
* ▶️ Play / Pause media
* ⏭️ Next track
* ⏮️ Previous track
* 🔊 Touchless volume control
* 📏 Pinch-distance based volume mapping
* 🛡️ Activation delay to reduce accidental triggers
* 📊 On-screen HUD and FPS display

## 🚀 Usage

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd virtual-knob
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the controller

```bash
python main.py
```

Make sure your webcam is connected and accessible before starting the application.

## 🖐️ Gesture Controls

| Gesture                             | Hand   | Action                    |
| ----------------------------------- | ------ | ------------------------- |
| 🤏 Web-shooter / activation gesture | Either | Activate controller       |
| ✊ Fist                              | Either | Play / Pause              |
| 🤙 Shaka                            | Right  | Next track                |
| 🤙 Shaka                            | Left   | Previous track            |
| 🖐️ Open palm                       | Either | Enter volume-control mode |
| 🤏 Pinch                            | Either | Adjust volume             |

### Activation

Perform the activation gesture and hold it for approximately **1 second**.

Once activated, the controller enters the gesture-control session.

The activation delay is intentional to prevent accidental activation.

### Media Controls

**Fist**

Close your hand into a fist to toggle:

```text
Play ↔ Pause
```

**Right-hand Shaka**

Use the thumb + pinky gesture with your **right hand** to skip to the next track.

**Left-hand Shaka**

Use the same gesture with your **left hand** to go to the previous track.

### Volume Control

Show an **open palm** to enter volume-control mode.

Then use a **pinching gesture** between your thumb and index finger.

The distance between the two fingers is measured in pixels:

```text
Thumb ●────────● Index
          ↑
     pixel distance
```

The measured distance is mapped to the system volume range:

```text
finger distance
       ↓
pixel measurement
       ↓
volume mapping
       ↓
system volume
```

Moving the fingers closer or farther apart changes the volume.

## ⚙️ How It Works

The application uses the webcam to capture frames and detect hand landmarks.

The processing pipeline is roughly:

```text
Webcam
   ↓
OpenCV
   ↓
Hand Landmark Detection
   ↓
Gesture Recognition
   ↓
Gesture Session
   ↓
Action Mapping
   ↓
System Media / Volume Control
```

The project is divided into separate modules:

```text
main.py
hand_tracker.py
finger_state.py
gestures.py
gesture_session.py
volume_control.py
ui.py
```

### Main Components

**`hand_tracker.py`**

Handles webcam frames and hand landmark detection.

**`finger_state.py`**

Determines finger states and higher-level gestures.

**`gestures.py`**

Contains gesture detection, pinch-distance calculation and volume mapping.

**`gesture_session.py`**

Manages activation and the current gesture-control session.

**`volume_control.py`**

Handles reading and changing the system volume.

**`ui.py`**

Draws the HUD and calculates/display FPS.

**`main.py`**

Connects all components and runs the main control loop.

## 🛠️ Tech Stack

* **Python**
* **OpenCV** — webcam processing
* **MediaPipe** — hand landmark detection
* **PyAutoGUI** — keyboard/media interaction
* **NumPy** — numerical operations
* **Windows Core Audio / audio controller** — system volume control

## ⚠️ Notes

* A working webcam is required.
* Good lighting improves gesture detection.
* Keep your hand clearly visible to the camera.
* The controller is currently designed around a fixed camera position and controlled environment.
* Gesture recognition may occasionally produce false positives depending on lighting, hand position and camera quality.

## 🔮 Future Improvements

* Better gesture robustness
* Calibration for different users and camera positions
* Improved filtering/smoothing for volume control
* More media controls
* Customizable gestures
* Support for additional operating systems
* Machine-learning based gesture classification
