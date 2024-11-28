import numpy as np

class vec3:
    e = [None]*3

    #def __init__(self):
    #    self.e = [0,0,0]
    
    def __init__(self, e0: float, e1: float, e2: float):
        self.e = [e0, e1, e2]
    
    def x(self): return self.e[0]
    def y(self): return self.e[1]
    def z(self): return self.e[2]

    def __neg__(self):
        return vec3(-self.e[0],-self.e[1],-self.e[2])
    
    def __getitem__(self, i: int):
        return self.e[i]
    
    def __iadd__(self, v):
        self.e[0] += v.e[0]
        self.e[1] += v.e[1]
        self.e[2] += v.e[2]
        return self
    
    def __imul__(self, t: float):
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self
    
    def __idiv__(self, t: float):
        self *= 1/t
    
    def length_squared(self) -> float:
        return self.e[0]**2 + self.e[1]**2 + self.e[2]**2
    
    def length(self):
        return np.sqrt(self.length_squared())
    
    def __add__(self, v):
        return vec3(self.e[0] + v.e[0], self.e[1] + v.e[1], self.e[2] + v.e[2])
    
    def __sub__(self, v):
        return vec3(self.e[0] - v.e[0], self.e[1] - v.e[1], self.e[2] - v.e[2])
    
    def __mul__(self, v):
        return vec3(self.e[0] * v.e[0], self.e[1] * v.e[1], self.e[2] * v.e[2])
    
    def __mul__(self, t: float):
        return vec3(t*self.e[0], t*self.e[1], t*self.e[2])
    
    def __truediv__(self, t: float):
        return self * (1/t)
    
def dot(u: vec3, v: vec3) -> float: 
    return u.e[0]*v.e[0] + u.e[1]*v.e[1] + u.e[2]*v.e[2]

def cross(u: vec3, v: vec3) -> vec3:
    return vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
                u.e[2] * v.e[0] - u.e[0] * v.e[2],
                u.e[0] * v.e[1] - u.e[1] * v.e[0])

def unit_vector(v: vec3) -> vec3 :
    return v / v.length()