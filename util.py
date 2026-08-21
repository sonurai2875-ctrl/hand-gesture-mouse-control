import numpy as np

def get_angle(a,b,c):
    radians=np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle=np.abs(radians*180.0/np.pi)
    return angle
def get_distance(landmarks_list):
    if len(landmarks_list) < 2:
        return None
    
    (x1, y1), (x2, y2) = landmarks_list[:2]
    distance = np.hypot(x1 - x2, y1 - y2)
    return np.interp(distance, [0, 1], [0, 1000])
