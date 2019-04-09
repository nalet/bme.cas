import numpy as np
import scipy as sp
from scipy import spatial

def paired_points_matching(source, target):
    """
    Calculates the transformation T that maps the source to the target
    :param source: A N x 3 matrix with N 3D points
    :param target: A N x 3 matrix with N 3D points
    :return:
        T: 4x4 transformation matrix mapping source onto target
        R: 3x3 rotation matrix part of T
        t: 1x3 translation vector part of T
    """
    assert source.shape == target.shape
    T = np.eye(4)
    R = np.eye(3)
    t = np.zeros((1, 3))

    m = source.shape[1]

    centroid_A = np.mean(source, axis=0)
    centroid_B = np.mean(target, axis=0)
    AA = source - np.mean(source, axis=0)
    BB = target - np.mean(target, axis=0)

    H = np.dot(AA.T, BB)
    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    if np.linalg.det(R) < 0:
       Vt[m-1,:] *= -1
       R = np.dot(Vt.T, U.T)

    t = centroid_B.T - np.dot(R,centroid_A.T)

    T = np.identity(m+1)
    T[:m, :m] = R
    T[:m, m] = t

    return T, R, t


def find_nearest_neighbor(src, dst):
    """
    Finds the nearest neighbor of every point in src in dst
    :param src: A N x 3 point cloud
    :param dst: A N x 3 point cloud
    :return: the
    """
    return sp.spatial.KDTree(dst).query(src)


def icp(source, target, init_pose=None, max_iterations=50, tolerance=0.0001):
    """
    Iteratively finds the best transformation that mapps the source points onto the target
    :param source: A N x 3 point cloud
    :param target: A N x 3 point cloud
    :param init_pose: A 4 x 4 transformation matrix for the initial pose
    :param max_iterations: default 10
    :param tolerance: maximum allowed error
    :return: A 4 x 4 rigid transformation matrix mapping source to target
            the distances and the error
    """
    T = np.eye(4)
    distances = 0
    error = 0

    e = 50
    p = 0

    # Your code goes here
    src_init = np.dot(init_pose[:3, :3], source.T).T
    src_init = src_init + np.tile(init_pose[:3, 3], (source.shape[0], 1))

    current_target = np.zeros_like(source)

    if init_pose is None:
        T = np.eye(4)
    else:
        T = init_pose

    current_tolerance = np.inf
    current_error = np.inf
    error = np.inf

    i = 0

    while current_tolerance > tolerance and i < max_iterations:
        distances, idx = find_nearest_neighbor(src_init, target)
        for ii, el in enumerate(idx):
            current_target[ii] = target[el]

        current_T, current_R, current_t = paired_points_matching(src_init, current_target)

        src_init = np.dot(current_R, src_init.T).T
        src_init = src_init + np.tile(current_t, (source.shape[0], 1))
        T = np.dot(current_T, T)

        current_error = error
        error = np.sqrt(np.sum(distances) / distances.shape[0])
        current_tolerance = current_error - error

        print ("Current: " + str(i) + " of max" + str(max_iterations) + " current tolerance: " + str(current_tolerance) + " tolerance: " + str(tolerance), end="\r")

        i += 1

    return T, distances, error


def get_initial_pose(template_points, target_points):
    """
    Calculates an initial rough registration
    (Optionally you can also return a hand picked initial pose)
    :param source:
    :param target:
    :return: A transformation matrix
    """
    T = np.eye(4)

    # Your code goes here
    T[:3, 3] = np.mean(target_points, axis=0) - np.mean(template_points, axis=0)

    return T