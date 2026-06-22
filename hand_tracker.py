import cv2
import mediapipe as mp
import json
FINGER_TIPS = [8,12,16,20]
FINGER_BASIS = [5,9,13,17]

def fingers_up(lm_list):
    if not lm_list:
        return[0,0,0,0]
    fingers = []
    for tip_id,base_id in zip(FINGER_TIPS,FINGER_BASIS):
        tip_y = lm_list[tip_id][2]
        base_y = lm_list[base_id][2]
        if tip_y<base_y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers


class HandTracker:
    def __init__(self, max_hands=1, detection_conf=0.7, tracking_conf=0.7):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )
        self.results = None

    def find_hands(self, frame, draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame,hand_lms,self.mp_hands.HAND_CONNECTIONS)
        return frame
    def landmark_list(self,frame,hand_index=0):
        landmark_list = []
        if self.results.multi_hand_landmarks:
            if hand_index < len(self.results.multi_hand_landmarks):
                hand = self.results.multi_hand_landmarks[hand_index]
                h,w,_ = frame.shape
                for id,lm in enumerate(hand.landmark):
                    px,py = int(lm.x*w),int(lm.y*h)
                    landmark_list.append([id,px,py])
        return landmark_list

def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    while True:
        sucess, frame = cap.read()
        if not sucess : break
        frame = cv2.flip(frame,1)
        frame = tracker.find_hands(frame)
        lm_list = tracker.landmark_list(frame)
        state = fingers_up(lm_list)
        print(state)
        # state_json = json.dump(state)
        cv2.putText(frame,str(state),(40,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
        # if lm_list:
            # tip_y = lm_list[8][2]
            # base_y = lm_list[5][2]
            # if tip_y<base_y:
            #     print("Index finger is UP")
            #     cv2.putText(frame,"Index finger is UP",(40,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
            # else:
            #     cv2.putText(frame,"Index finger is DOWN",(40,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
            
            # if lm_list[4][1]>lm_list[3][1]:
            #     cv2.putText(frame,"Thumb extended",(60,60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
            # x,y = lm_list[8][1],lm_list[8][2]
            # cv2.circle(frame,(x,y),12,(0,0,255),cv2.FILLED)
            # cv2.putText(frame,f"({x},{y})",(x+15,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)

        cv2.imshow("Virtual Knob",frame)
        if cv2.waitKey(1)==ord("q"):break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()