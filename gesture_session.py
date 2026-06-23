import time

class GestureSession:
    def __init__(self,arm_duration,grace_period):
        self.armed  = False
        self.expire_at = 0 
        self.arm_duration = arm_duration
        self.grace_period = grace_period
        self.wait_until = 0
    
    def is_waiting(self):
        return time.time()<self.wait_until
    
    def try_arm(self, force = False):
        self.armed = True
        self.expire_at = time.time()+self.arm_duration
        self.wait_until = time.time()+ self.grace_period

    def extend(self):
        if self.armed:
            self.expire_at  = time.time()+self.arm_duration

    def update(self):
        if self.armed :
            if self.is_waiting():
                self.expire_at = time.time()+ self.arm_duration
            elif time.time()>self.expire_at:
                self.armed = False
    
    def time_left(self):
        if not self.armed:
            return 0
        return max(0,self.expire_at - time.time())
    
    def progress(self):
        if not self.armed:
            return 0.0
        return self.time_left()/self.arm_duration
    
    def kill(self):
        self.armed = False

    
