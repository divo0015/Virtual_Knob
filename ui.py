import cv2
import time

_prev_time = 0

def draw_hud(frame , session, vol_pct, gesture, fps):
    h,w,_ = frame.shape
    overlay = frame.copy()
    cv2.rectangle(overlay,(0,0),(w,52),(0,0,0),-1)
    cv2.addWeighted(overlay,0.45,frame, 0.55,0, frame)
    cv2.putText(frame, f"{int(fps)} fps",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.55,(150,150,150),1)
    state_text = "WAIT" if session.is_waiting() else ("ACTIVE" if session.armed else "LOCKED")
    state_color = (0,255,255) if session.is_waiting() else ((0,255,0) if session.armed else (0,0,255))
    cv2.putText(frame, state_text, (w-110,20),cv2.FONT_HERSHEY_SIMPLEX,0.55,state_color,1)
    if gesture:
        cv2.putText(frame,gesture,(w//2-60,35),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255,255,255),2)

    draw_volume_bar(frame,vol_pct)

def draw_volume_bar(frame, vol_pct):
    h,w,_ = frame.shape
    bar_x, bar_y = 20,h-30
    bar_w, bar_h = w - 40,10
    cv2.rectangle(frame, (bar_x,bar_y),(bar_x+bar_w,bar_y+bar_h),(60,60,60),-1)
    fill_w = int(bar_w*vol_pct/100)
    if vol_pct< 40:
        color = (0,200,0)
    elif vol_pct< 75:
        color = (0,200,255)
    else:
        color = (0,80,255)
    cv2.rectangle(frame,(bar_x,bar_y),(bar_x + fill_w,bar_y+bar_h),color,-1)

    cv2.putText(frame,f"vol{int(vol_pct)}%",(bar_x,bar_y-6),cv2.FONT_HERSHEY_SIMPLEX,0.45,(180,180,180),1)

def calc_fps(prev_time):
    curr = time.time()
    fps = 1/(curr - prev_time+ 1e-9)
    return fps,curr


# def draw_session_ring(frame,session):
#     h,w,_ = frame.shape
#     center = (w-60,60)
#     radius = 35

#     cv2.ellipse(frame,center,(radius,radius),0,0,360,(60,60,60),4)

#     if session.armed:
#         sweep_angle = 360* session.progress()
#         cv2.ellipse(frame,center,(radius,radius),-90,0,sweep_angle,(0,255,0),4)
#         label = f"{session.time_left():.1f}s"
#         color=(0,255,0)
#     else:
#         label = "LOCKED"
#         color=(0,0,255)
    
#     cv2.putText(frame,label,(center[0]-28,center[1]+5),cv2.FONT_HERSHEY_SIMPLEX,0.45,color,1)