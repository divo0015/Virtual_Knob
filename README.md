# 🤙 Virtual Knob
Control media playback and system volume using hand gestures — no keyboard, no mouse.

Built with Python, OpenCV, and MediaPipe.

---

## Gestures

| Gesture | Action |
|---|---|
| 🤙 Web-shooter sign (index + pinky up) | **Arm the system** |
| ✊ Fist held for ~0.3s | **Play / Pause** |
| 🤏 Thumb + index pinch | **Volume control** (spread = louder, close = quieter) |
| Spacebar | **Arm the system** (keyboard shortcut) |
| Q | **Quit** |

### How activation works
The system is **LOCKED** by default and ignores all gestures.
Show the web-shooter sign (or press spacebar) to **ARM** it.
A 2-second grace period starts (cyan ring), then the system goes **ACTIVE** (green ring).
The session auto-locks after a few seconds of no gesture activity.

---

## Installation

### Requirements
- Python 3.9 or higher
- A webcam
- Windows (see Mac section below for differences)

### Step 1 — Clone or download the project
```bash
git clone https://github.com/yourname/virtual-knob
cd virtual-knob
```

### Step 2 — Create a virtual environment (recommended)
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### Step 3 — Install dependencies

**Windows:**
```bash
pip install opencv-python mediapipe pyautogui numpy pycaw comtypes
```

**Mac:**
```bash
pip install opencv-python mediapipe pyautogui numpy
```
> Mac uses the built-in `osascript` for volume — no extra install needed.
> Swap `volume_control.py` for the Mac version (see below).

### Step 4 — Run
```bash
python main.py
```

---

## Mac Compatibility

| Feature | Windows | Mac |
|---|---|---|
| Hand detection | ✅ | ✅ |
| Gesture activation | ✅ | ✅ |
| Play / Pause | ✅ | ✅ |
| Volume control | ✅ pycaw | ✅ osascript (no install) |
| Webcam feed + HUD | ✅ | ✅ |

**To run on Mac:** replace `volume_control.py` with the Mac version that uses
`subprocess` + `osascript` instead of pycaw. Everything else is identical.

---

## File Structure

```
virtual_knob/
├── main.py              # Entry point — main loop and activation logic
├── hand_tracker.py      # HandTracker class wrapping MediaPipe Hands
├── finger_state.py      # fingers_up(), is_arm_gesture()
├── gesture_session.py   # GestureSession — armed/locked state machine
├── gestures.py          # check_fist(), pinch detection, smoothing
├── volume_control.py    # System volume wrapper (pycaw on Windows)
└── ui.py                # HUD overlay — ring, volume bar, FPS, labels
```

---

## Tuning

If gestures feel too sensitive or not sensitive enough, adjust these
constants at the top of each file:

**gestures.py**
```python
FIST_HOLD_FRAMES    = 8     # frames fist must be held (~0.3s at 30fps)
PINCH_MIN           = 25    # pixel distance = 0% volume
PINCH_MAX           = 200   # pixel distance = 100% volume
PINCH_ACTIVE_THRESHOLD = 80 # below this = intentional pinch
```

**gesture_session.py**
```python
arm_duration  = 6.0   # seconds session stays active
grace_period  = 2.0   # seconds to wait after arming before gestures fire
```

To find your real PINCH_MIN and PINCH_MAX:
1. Add `print(get_pinch_distance(lm_list))` in your loop temporarily
2. Pinch fingers fully closed → note the value → that's your MIN
3. Spread thumb and index fully apart → note the value → that's your MAX

---

## Planned Features
- [ ] Next track gesture
- [ ] Previous track gesture
- [ ] On-screen gesture guide overlay
- [ ] Config file for thresholds (no code editing needed)

---

## Troubleshooting

**Camera not opening**
Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` in `main.py`.
Run this to find the right index:
```python
import cv2
for i in range(4):
    cap = cv2.VideoCapture(i)
    print(f"Index {i}: {'works' if cap.read()[0] else 'no camera'}")
    cap.release()
```

**MediaPipe import error**
```bash
pip uninstall mediapipe -y
pip install mediapipe==0.10.9
```

**pycaw error on Windows**
```bash
pip install pycaw comtypes
```
Make sure you're running from inside your virtual environment.

**Gestures fire too easily / not at all**
Print your raw values first, then tune the constants in `gestures.py`.
See the Tuning section above.

---

## Dependencies

| Package | Version tested | Purpose |
|---|---|---|
| opencv-python | 4.9+ | Webcam feed and drawing |
| mediapipe | 0.10.9 | Hand landmark detection |
| pyautogui | 0.9+ | Play/pause media key |
| numpy | 1.24+ | Interpolation and smoothing |
| pycaw | 0.0.8 | Windows volume control |
| comtypes | 1.2+ | Required by pycaw on Windows |


For Mac Users, 
change the code in the file named "volume_control.py" 

from ctypes import cast,POINTER 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
def get_volume_controller():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast (interface , POINTER(IAudioEndpointVolume))
    return volume 

def set_volume(volume_ctrl , level_float):
    level_float = max(0.0, min (1.0,level_float))
    volume_ctrl.SetMasterVolumeLevelScalar(level_float,None)

def get_volume(volume_ctrl):
    return volume_ctrl.GetMasterVolumeLevelScalar()
