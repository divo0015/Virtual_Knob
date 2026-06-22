from ctypes import cast,POINTER 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
def get_volume_controller():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast (interface , POINTER(IAudioEndpointVolume))
    return volume 

def set_volume(volume_ctrl , level_float):
    level_float = max(0.0, min (1.0,level_float))
    volume_ctrl.SetMasterVolumeLevelScalar(level_float,None)

def get_volume(volume_ctrl):
    return volume_ctrl.GetMasterVolumeLevelScalar()
