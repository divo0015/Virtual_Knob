
FINGER_TIPS = [8,12,16,20]
FINGER_BASES = [5,9,13,17]
FINGER_NAMES = ["index","middle","ring","pinky"]

def fingers_up(lm_list):
    if not lm_list:
        return [0,0,0,0]
    fingers = []
    for tip_id,base_id in zip(FINGER_TIPS,FINGER_BASES):
        fingers.append(1 if lm_list[tip_id][2]<lm_list[base_id][2] else 0)
    return fingers

def is_index_up(lm_list):
    if not lm_list:
        return False
    return lm_list[8][2]<lm_list[5][2]

def get_index_tip_pos(lm_list):
    if not lm_list:
        return None
    return (lm_list[8][1],lm_list[8][2])

def is_arm_gesture(lm_list):
    if not lm_list:
        return False
    state = fingers_up(lm_list)
    return state == [1,0,0,1]


