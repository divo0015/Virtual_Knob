import cv2
import pyautogui
from hand_tracker import HandTracker
from finger_state import fingers_up, is_arm_gesture
from gesture_session import GestureSession
from ui import draw_hud,calc_fps
from gestures import check_fist, get_pinch_distance, pinch_to_volume, draw_pinch_line
from volume_control import set_volume, get_volume, get_volume_controller

import numpy as np


def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    session = GestureSession(3.0,2.0)
    vol = get_volume_controller()
    prev_t = 0
    vol_pct = int(get_volume(vol)*100)


    while True:
        sucess, frame = cap.read()
        if not sucess:
            break
        frame = cv2.flip(frame, 1)

        frame = tracker.find_hands(frame)
        lm_list = tracker.landmark_list(frame)
        fps, prev_t = calc_fps(prev_t)


        key = cv2.waitKey(1)

        session.update()
        gesture = None
        if not session.armed:
            if is_arm_gesture(lm_list):
                session.try_arm()
            if key == ord(" "):
                session.try_arm()
        else:
            if check_fist(lm_list):
                pyautogui.press("playpause")
                session.kill()
                gesture = "play / pause"
            if not session.is_waiting():
                dist = get_pinch_distance(lm_list)
                if dist is not None:
                    vol_float = pinch_to_volume(dist)
                    t = (lm_list[4][1], lm_list[4][2])
                    i = (lm_list[8][1], lm_list[8][2])
                    mid = ((t[0]+i[0])//2, (t[1]+i[1])//2)
                    vol_pct = np.interp(dist, [25, 200], [0, 100])
                    cv2.putText(
                        frame, f"{int(vol_pct)}%", (mid[0]+20, mid[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    # print("vol_float =", vol_float, type(vol_float))
                    set_volume(vol, pinch_to_volume(dist))
                    draw_pinch_line(frame,lm_list)
                    gesture = "volume"
            else:
                gesture = "get ready..."
        if key == ord("q"):
            break

        draw_hud(frame,session,vol_pct,gesture, fps)
        cv2.imshow("Virtual Knob", frame)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
