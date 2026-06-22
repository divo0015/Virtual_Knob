from volume_control import get_volume_controller , set_volume, get_volume

vol = get_volume_controller()
print("Current Volume:",get_volume(vol))
set_volume(vol,0.3)
print("set volume to 30%")