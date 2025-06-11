import numpy as np

class Matrices:    
    def translate(self, x, y, z):

        translation = np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]])
        
        return translation
    
    def rotate(self, r):

        rrx, rry, rrz = np.radians(r[0]), np.radians(r[1]), np.radians(r[2])
        
        rot_x = np.array([
            [1,            0,           0, 0],
            [0,  np.cos(rrx), np.sin(rrx), 0],
            [0, -np.sin(rrx), np.cos(rrx), 0],
            [0,            0,           0, 1]])

        rot_y = np.array([
            [np.cos(rry), 0, -np.sin(rry), 0],
            [          0, 1,            0, 0],
            [np.sin(rry), 0,  np.cos(rry), 0],
            [          0, 0,            0, 1]])

        rot_z = np.array([
            [np.cos(rrz), -np.sin(rrz), 0, 0],
            [np.sin(rrz),  np.cos(rrz), 0, 0],
            [          0,            0, 1, 0],
            [          0,            0, 0, 1],])

        
        return rot_x @ rot_y @ rot_z
    
    def rotate_around_p(self, p=(0,0,0), r=(0,0,0)):

        # p in form (x_offset, y_offset, z_offset)
        # NOTE : for some reason, y and z switch in calculations
        # thus, p gets deconstructed as :
        px, pz, py = p

        #re_translate =   self.translate(px, py, pz) @ self.right_handed
        #anti_translate = self.translate(-px, -py, -pz) @ self.right_handed


        return_to_pos =   Matrices.translate(self, px, py, pz)
        translate_to_zero = Matrices.translate(self, -px, -py, -pz)

        rotate = Matrices.rotate(self, r)


        k = return_to_pos @ rotate @ translate_to_zero

        return k