import numpy as np
dist = 80
 
vol_pct = np.interp(dist,[25,200],[0,100])
print(vol_pct)
vol_float = np.interp(dist,[25,200],[0.0,1.0])
print(vol_float)