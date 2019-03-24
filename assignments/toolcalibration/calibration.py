import numpy as np


def pivot_calibration(transforms):
    """ Pivot calibration
    Keyword arguments:
    transforms -- A list with 4x4 transformation matrices
    returns -- A vector p_t, which is the offset from any T to the pivot point
    """

    p_t = np.zeros((3, 1))
    T = np.eye(4)
    A = []
    b = []

    for item in transforms:
        A.append(np.append(item[0,[0,1,2]],[-1,0,0]))
        A.append(np.append(item[1,[0,1,2]],[0,-1,0]))
        A.append(np.append(item[2,[0,1,2]],[0,0,-1]))
        b.append((item[0,[3]]))
        b.append((item[1,[3]]))
        b.append((item[2,[3]]))

    x = np.linalg.lstsq(A,b,rcond=None)

    result = (x[0][0:3]).flatten()*-1
    result = [result]

    p_t = np.asarray(result).transpose()
    T[:3, 3] = p_t.T
    
    return p_t, T
