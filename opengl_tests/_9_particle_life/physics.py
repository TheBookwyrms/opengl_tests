import numpy as np


def do_physics(points_array, dt):

    points_array = list(points_array)

    all_f_total = []

    for i in points_array:
        f_total = np.array([0, 0]).astype(np.float32)
        for k, j in enumerate(points_array):
            if i==j:
                continue
            i_s, j_s = i.data[:2], j.data[:2]

            dist_vec = j_s-i_s
            dist = np.linalg.norm(dist_vec)
            if dist<0.0001:
                points_array.pop(k)
                continue
            dist_unit_vec = dist_vec/dist

            beta = 3
            a=1
            if dist < beta:
                f = (dist_unit_vec/beta)-1
            elif dist < 1:
                f = a*(1-(np.abs(2*dist_unit_vec-1-beta)/(1-beta)))
            else:
                f = np.array([0, 0])
            
            f_total += f
        all_f_total.append(f_total)

    for i, j in enumerate(points_array):
        j.data[:2] += all_f_total[i]*dt*dt
                

    return np.array(points_array)