import cv2
import pyautogui
from hand_tracker import HandTracker
from finger_state import fingers_up, is_arm_gesture
from gesture_session import GestureSession
from ui import draw_session_ring
from gestures import check_fist,get_pinch_distance,pinch_to_volume,draw_pinch_line
from volume_control import set_volume , get_volume,get_volume_controller
import numpy as np
def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    session = GestureSession(arm_duration=6.0)
    vol = get_volume_controller()

    while True:
        sucess , frame = cap.read()
        if not sucess : break
        frame = cv2.flip(frame,1)

        frame = tracker.find_hands(frame)
        lm_list = tracker.landmark_list(frame)


        key = cv2.waitKey(1)
        

        session.update()
        if not session.armed:
            if is_arm_gesture(lm_list):
                session.try_arm()
            if key == ord(" "):
                session.try_arm()
        else:
            print("active")
            # session.start_wait(2)
            if check_fist(lm_list):
                pyautogui.press("playpause")
                session.kill()
            if not session.is_waiting():
                dist = get_pinch_distance(lm_list)
                if dist is not None:
                    vol_float = pinch_to_volume(dist)
                    # cv2.putText(frame,f"{vol_float*100:.0f}",(mid[0]+10,mid[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5)
                    print("vol_float =", vol_float, type(vol_float))
                    set_volume(vol,vol_float)
                # session.extend()
            # if is_arm_gesture(lm_list):session.extend()
        if key == ord("q"): break

        draw_session_ring(frame,session)
        cv2.imshow("Virtual Knob",frame)
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
