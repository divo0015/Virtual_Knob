import cv2
import pyautogui
from hand_tracker import HandTracker
from finger_state import fingers_up, is_arm_gesture, check_shaka
from gesture_session import GestureSession
from ui import draw_hud, calc_fps
from gestures import (check_fist, check_open_palm,
                      get_smooth_pinch_distance, pinch_to_volume,
                      draw_pinch_line)
from volume_control import set_volume, get_volume, get_volume_controller
import numpy as np


def main():
    cap         = cv2.VideoCapture(0)
    tracker     = HandTracker()
    session     = GestureSession(3.0, 2.0)
    vol         = get_volume_controller()
    prev_t      = 0
    vol_pct     = int(get_volume(vol) * 100)
    volume_mode = False

    while True:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)

        frame       = tracker.find_hands(frame)
        lm_list     = tracker.landmark_list(frame)
        handedness  = tracker.get_handedness()  
        fps, prev_t = calc_fps(prev_t)

        key = cv2.waitKey(1) & 0xFF
        session.update()
        gesture = None

        if not session.armed:
            volume_mode = False
            if is_arm_gesture(lm_list): session.try_arm()
            if key == ord(" "):         session.try_arm()

        elif session.is_waiting():
            gesture = "get ready..."

        else:
            # ── priority 1: fist ──────────────────────────────
            if check_fist(lm_list):
                if volume_mode:
                    volume_mode = False
                    gesture = "volume OFF"
                else:
                    pyautogui.press("playpause")
                    session.kill()
                    gesture = "play / pause"

            # ── priority 2: shaka → next or prev ──────────────
            elif check_shaka(lm_list):
                # flipped frame: MediaPipe 'Left' = user's RIGHT hand
                if handedness == "Right":
                    pyautogui.press("nexttrack")
                    session.kill()
                    gesture = "next track ->"
                elif handedness == "Left":
                    pyautogui.press("prevtrack")
                    session.kill()
                    gesture = "<- prev track"

            # ── priority 3: open palm → enter volume mode ─────
            elif check_open_palm(lm_list) and not volume_mode:
                volume_mode = True
                session.extend()
                gesture = "volume mode ON"

            # ── priority 4: pinch → adjust volume ─────────────
            elif volume_mode:
                dist      = get_smooth_pinch_distance(lm_list)
                vol_float = pinch_to_volume(dist)
                set_volume(vol, vol_float)
                vol_pct = int(vol_float * 100)
                t   = (lm_list[4][1], lm_list[4][2])
                i   = (lm_list[8][1], lm_list[8][2])
                mid = ((t[0]+i[0])//2, (t[1]+i[1])//2)
                cv2.putText(frame, f"{int(vol_pct)}%",
                            (mid[0]+20, mid[1]),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255), 2)
                draw_pinch_line(frame, lm_list)
                gesture = f"volume {int(vol_pct)}%"

            if not session.armed:
                volume_mode = False

        if key == ord("q"):
            break

        draw_hud(frame, session, vol_pct, gesture, fps)
        cv2.imshow("Virtual Knob", frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()