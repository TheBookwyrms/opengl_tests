import numpy as np

def make_rot_mat(vector_axis, rotation_angle_rad):
    normalised_vec = vector_axis/np.linalg.norm(vector_axis)
    ux, uy, uz = normalised_vec

    cos = lambda theta : np.cos(theta)
    sin = lambda theta : np.sin(theta)

    th = rotation_angle_rad

    rot_mat = np.array([
        [cos(th) + ux**2*(1-cos(th)), ux*uy*(1-cos(th))-uz*sin(th), ux*uz*(1-cos(th))+uy*sin(th)],
        [uy*ux*(1-cos(th))+uz*sin(th), cos(th) + uy**2*(1-cos(th)), uy*uz*(1-cos(th))+ux*sin(th)],
        [uz*ux*(1-cos(th))+uy*sin(th), uz*uy*(1-cos(th))+ux*sin(th), cos(th) + uz**2*(1-cos(th))],
    ])

    return rot_mat