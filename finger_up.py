FINGER_TIPS = [8, 12, 16, 20]
FINGER_BASIS = [5, 9, 13, 17]


def fingers_up(lm_list):
    if not lm_list:
        return [0, 0, 0, 0]
    fingers = []
    for tip_id, base_id in zip(FINGER_TIPS, FINGER_BASIS):
        tip_y = lm_list[tip_id][2]
        base_y = lm_list[base_id][2]
        if tip_y < base_y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers
