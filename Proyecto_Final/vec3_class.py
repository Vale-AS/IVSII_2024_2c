import numpy as np
from rtweekend import random_double

class vec3:
    e = [None]*3

    #def __init__(self):
    #    self.e = [0,0,0]
    
    #def __init__(self, e0: float, e1: float, e2: float):
    #    #self.e = [e0, e1, e2]
    #    self.e = np.array([e0,e1,e2])

    def __init__(self, coords: np.ndarray):
        self.e = coords
    
    def x(self): return self.e[0]
    def y(self): return self.e[1]
    def z(self): return self.e[2]

    def __neg__(self):
        #return vec3(-self.e[0],-self.e[1],-self.e[2])
        
        #neg_e = np.negative(self.e)
        #return vec3(neg_e[0],neg_e[1],neg_e[2])
        return vec3(np.negative(self.e))
    
    def __getitem__(self, i: int):
        return self.e[i]
    
    def __iadd__(self, v):
        #self.e[0] += v.e[0]
        #self.e[1] += v.e[1]
        #self.e[2] += v.e[2]
        self.e += v.e
        return self
    
    def __imul__(self, t: float):
        self.e *= 2
        return self
    
    def __idiv__(self, t: float):
        self.e /= t
        return self
    
    def length_squared(self) -> float:
        #return self.e[0]**2 + self.e[1]**2 + self.e[2]**2
        return np.dot(self.e, self.e)
    
    def length(self):
        return np.sqrt(self.length_squared())
    
    def near_zero(self):
        return np.allclose(self.e, np.zeros(3))

    def __add__(self, v):
        #return vec3(self.e[0] + v.e[0], self.e[1] + v.e[1], self.e[2] + v.e[2])

        #sum_e = self.e + v.e
        #return vec3(sum_e[0], sum_e[1], sum_e[2])
        return vec3(self.e + v.e)
    
    def __sub__(self, v):
        #return vec3(self.e[0] - v.e[0], self.e[1] - v.e[1], self.e[2] - v.e[2])

        #sub_e = self.e - v.e
        #return vec3(sub_e[0], sub_e[1], sub_e[2])
        return vec3(self.e - v.e)
    
    def __mul__(self, v):
        #return vec3(self.e[0] * v.e[0], self.e[1] * v.e[1], self.e[2] * v.e[2])

        #mul_e = self.e * v.e
        #return vec3(mul_e[0], mul_e[1], mul_e[2])

        return vec3(self.e * v.e)
    
    def __mul__(self, t):
        #return vec3(t*self.e[0], t*self.e[1], t*self.e[2])

        #mul_e = self.e * t
        #return vec3(mul_e[0], mul_e[1], mul_e[2])
        if isinstance(t, vec3):
            return vec3(self.e * t.e)
        else: 
            return vec3(self.e * t)
    
    def __truediv__(self, t: float):
        return self * (1/t)

    
def dot(u: vec3, v: vec3) -> float: 
    #return u.e[0]*v.e[0] + u.e[1]*v.e[1] + u.e[2]*v.e[2]
    return np.dot(u.e, v.e)

def cross(u: vec3, v: vec3) -> vec3:
    #return vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
    #            u.e[2] * v.e[0] - u.e[0] * v.e[2],
    #            u.e[0] * v.e[1] - u.e[1] * v.e[0])

    cross_e = np.linalg.cross(u.e, v.e)
    return vec3(cross_e[0], cross_e[1], cross_e[2])


def unit_vector(v: vec3) -> vec3 :
    norm = np.linalg.norm(v.e)
    if norm == 0:
        return v
    else:
        return v / norm
    
    #return v / v.length()#return v / v.length()

def random(min: float = 0, max: float = 1):
        return vec3(np.array([random_double(min, max), random_double(min, max), random_double(min, max)]))

def random_unit_vector():
    while(True):
        p = random(-1,1)
        lensq = p.length_squared()
        if 1e-160 < lensq and lensq <= 1:
            return p / np.sqrt(lensq)

def random_on_hemisphere(normal: vec3):
    on_unit_sphere = random_unit_vector()
    if (dot(on_unit_sphere, normal) > 0.0): # in same hemisphere as normal
        return on_unit_sphere
    else:
        return -on_unit_sphere

def reflect(v: vec3, n:vec3):
    return v - n*dot(v,n)*2