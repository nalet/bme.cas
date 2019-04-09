import numpy as np
import scipy as sp
from scipy import spatial
import matplotlib.pyplot as plt
import cas.registration.util as util
import matplotlib.animation as animation

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

    tmp_trg = np.zeros_like(source)

    if init_pose is None:
        T = np.eye(4)
    else:
        T = init_pose

    tmp_tol = np.inf
    error = np.inf

    i = 0

    while tmp_tol > tolerance and i < max_iterations:
        distances, idx = find_nearest_neighbor(src_init, target)
        for ii, el in enumerate(idx):
            tmp_trg[ii] = target[el]

        T_tmp, R_tmp, t_tmp = paired_points_matching(src_init, tmp_trg)

        src_init = np.dot(R_tmp, src_init.T).T
        src_init = src_init + np.tile(t_tmp, (source.shape[0], 1))
        T = np.dot(T_tmp, T)

        err_tmp = error
        error = np.sum(distances) / distances.shape[0]
        error = np.sqrt(error)
        tmp_tol = err_tmp - error
        Animation.getInstance().animate(T, distances, error)

        i += 1
        

    print("Iterations: ", i)

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

class Animation:
    __instance = None
    target_points = util.read_data('data/registration/TargetPoints.csv')
    template_points = util.read_data('data/registration/TemplatePoints.csv')
    fig = None
    ax = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Animation.__instance == None:
            Animation()
        return Animation.__instance
    def __init__(self):
        """ Virtually private constructor. """
        if Animation.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Animation.__instance = self
            Animation.__instance.prepare()

    def prepare(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.ax.set_xlim3d([-1.0, 1.0])
        self.ax.set_ylim3d([-1.0, 1.0])
        self.ax.set_zlim3d([0.0, 10.0])

        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')
        plt.axis('equal')
        
    def animate(self, T, d, error):
        template_points_T = util.make_homogenous(self.template_points)
        template_points_T = np.dot(T, template_points_T.T).T[:, :3]    

        sample_choice = np.random.choice(self.target_points.shape[0], 1000)
        samples = self.target_points[sample_choice, :]
        self.ax.scatter(samples[:, 0], samples[:, 1], samples[:, 2], c='b', marker='.')
        self.ax.scatter(template_points_T[:, 0], template_points_T[:, 1], template_points_T[:, 2], c='r', marker='x')
        plt.show()