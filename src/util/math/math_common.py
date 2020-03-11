def clamp(v, min, max):
    v = min if v < min else v
    v = max if v > max else v
    return v

def overlap_bounds(bbox1, bbox2):
    amin, amax = bbox1
    bmin, bmax = bbox2
    overlap = True
    overlap = False if (amin.x > bmax.x or amax.x < bmin.x) else overlap
    overlap = False if (amin.y > bmax.y or amax.y < bmin.y) else overlap
    overlap = False if (amin.z > bmax.z or amax.z < bmin.z) else overlap
    return overlap

