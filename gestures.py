import math
import numpy as np
import cv2
from finger_state import fingers_up
from collections import deque

FIST_HOLD_FRAMES = 8
PINCH_MIN = 25
PINCH_MAX = 200
_pinch_history = deque(maxlen=5)
_fist_counter = 0

def get_smooth_pinch_distance(lm_list):
    dist = get_pinch_distance(lm_list)
    if dist is None:
        _pinch_history.clear()
        return None
    _pinch_history.append(dist)
    return sum(_pinch_history)/len(_pinch_history)

def check_fist(lm_list):
    global _fist_counter
    if not lm_list:
        _fist_counter = 0
        return False
    if fingers_up(lm_list) == [0,0,0,0]:
        _fist_counter+=1
    else:
        _fist_counter =0 
    if _fist_counter==FIST_HOLD_FRAMES:
        _fist_counter =0
        return True
    return False
def get_pinch_distance(lm_list):
    if not lm_list:
        return None
    tx,ty = lm_list[4][1],lm_list[4][2]
    ix,iy = lm_list[8][1],lm_list[8][2] 
    return math.hypot(ix-tx,iy-ty)

def pinch_to_volume(dist):
    return float(np.interp(dist,[PINCH_MIN,PINCH_MAX],[0.0,1.0]))

def draw_pinch_line(frame, lm_list):
    if not lm_list : return 
    t = (lm_list[4][1],lm_list[4][2])
    i = (lm_list[8][1],lm_list[8][2])
    mid = ((t[0]+i[0])//2,(t[1]+i[1])//2)
    cv2.line(frame,t,i,(0,0,255),2)
    cv2.circle(frame,t,8,(0,255,255),-1)
    cv2.circle(frame,i,8,(0,255,255),-1)
    cv2.circle(frame,mid,5,(255,255,255),-1)
