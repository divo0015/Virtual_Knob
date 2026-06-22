import cv2

def draw_session_ring(frame,session):
    h,w,_ = frame.shape
    center = (w-60,60)
    radius = 35

    cv2.ellipse(frame,center,(radius,radius),0,0,360,(60,60,60),4)

    if session.armed:
        sweep_angle = 360* session.progress()
        cv2.ellipse(frame,center,(radius,radius),-90,0,sweep_angle,(0,255,0),4)
        label = f"{session.time_left():.1f}s"
        color=(0,255,0)
    else:
        label = "LOCKED"
        color=(0,0,255)
    
    cv2.putText(frame,label,(center[0]-28,center[1]+5),cv2.FONT_HERSHEY_SIMPLEX,0.45,color,1)