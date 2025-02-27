import numpy as np


def new_physics_test(all_points_array, grid, dt):

    indices_to_pop = []

    for p1 in all_points_array:
        pgrid = p1.grid_square
        
        f_total = np.array([0, 0]).astype(np.float32)

        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                box_dist = pgrid-np.array([x, y])
                compare = True if ((box_dist[0] in [-1, 0, 1]) and (box_dist[1] in [-1, 0, 1])) else False
                
                if compare == True:
                    #print(grid[x, y])
                    for p2 in grid[x, y]:

                        if p1 == p2:
                            continue

                        p1_s, p2_s, = p1.data[:2], p2.data[:2]

                        dist_vec = p2_s-p1_s
                        dist = np.linalg.norm(dist_vec)

                        if dist<0.0001:
                            index = np.array(np.where(all_points_array == p2)).astype(int)
                            index = index[0][0]

                            p2.data[:2] = (
                                np.random.choice(list(range(1000, 10000, 25))),
                                np.random.choice(list(range(1000, 10000, 25)))
                                )
                            
                            indices_to_pop.append(index)

                            p1_s, p2_s, = p1.data[:2], p2.data[:2]

                            dist_vec = p2_s-p1_s
                            dist = np.linalg.norm(dist_vec)

                            continue

                        dist_unit_vec = dist_vec/dist

                        a = 0.1
                        beta = 0.2
                        colour_multiplier=p1.force_to[str(p2.colour)]
                        if dist < beta:
                            f = -((dist_unit_vec/beta)-3)
                        elif dist < 1:
                            f = a*colour_multiplier*(1-(np.abs(2*dist_unit_vec-1-beta)/(1-beta)))
                        else:
                            f = np.array([0, 0])
                        #print((1-(np.abs(2*dist_unit_vec-1-beta)/(1-beta))))
                        f_total += f

        #if f_total.all() != 0:
        #    f_u_v = f_total / np.linalg.norm(f_total)
        #    friction_dir = -1 * f_u_v
        #    friction = 0.1*f_total*friction_dir
        #    f_total += friction
        #    #print(f_total, friction)


        v_change = f_total*dt
        p1.v += v_change

        if np.linalg.norm(p1.v) > 4:
            p1.v /= np.linalg.norm(p1.v)

        pos_change = p1.v*dt
        p1.data[:2] += pos_change

    
    
    a2 = list(all_points_array)
    num_popped = 0
    for i in indices_to_pop:
        a2.pop(i-num_popped)
        num_popped += 1
    all_points_array = np.array(a2)

    return all_points_array




    #for index, comparisons in enumerate(comparison_array):
    #    #print(comparisons)
#
    #    p1 = all_points_array[index]
    #                
    #    f_total = np.array([0, 0]).astype(np.float32)
#
    #    for p2 in comparisons:
    #        #print(p1, p2, p1.data[:2], p2.data[:2]) '''important'''
    #        if p1 is p2:
    #            continue
    #        p1_s, p2_s, = p1.data[:2], p2.data[:2]
#
#
#
    #        #print(p1_s, p2_s)
    #        
    #        dist_vec = p2_s-p1_s
    #        dist = np.linalg.norm(dist_vec)
    #        dist_unit_vec = dist_vec/dist
#
    #        print(dist)
#
#
    #        beta = 3
    #        a=1
    #        if dist < beta:
    #            f = (dist_unit_vec/beta)-1
    #        elif dist < 1:
    #            f = a*(1-(np.abs(2*dist_unit_vec-1-beta)/(1-beta)))
    #        else:
    #            f = np.array([0, 0])
    #    
    #        f_total += f
#
    #    pos_change = f_total*dt*dt
#
    #    all_points_array[index].data[:2] += pos_change
#
    #
    ##print(all_points_array[0].data[:2])
#
    #
    #return all_points_array





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