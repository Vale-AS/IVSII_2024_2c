import numpy as np
from rtweekend import random_double
from numba import njit

class vec3:
    e = [None]*3

    def __init__(self, coords: np.ndarray):
        self.e = coords
    
    def x(self): return self.e[0]
    def y(self): return self.e[1]
    def z(self): return self.e[2]

    def __neg__(self):
        return vec3(np.negative(self.e))
    
    def __getitem__(self, i: int):
        return self.e[i]
    
    def __iadd__(self, v):
        self.e += v.e
        return self
    
    def __imul__(self, t: float):
        self.e *= 2
        return self
    
    def __idiv__(self, t: float):
        self.e /= t
        return self
    
    def length_squared(self) -> float:
        return np.dot(self.e, self.e)
    
    def length(self):
        return np.sqrt(self.length_squared())
    
    def near_zero(self):
        return np.allclose(self.e, np.zeros(3))

    def __add__(self, v):
        return vec3(self.e + v.e)
    
    def __sub__(self, v):
        return vec3(self.e - v.e)
    
    def __mul__(self, v):
        return vec3(self.e * v.e)
    
    def __mul__(self, t):
        if isinstance(t, vec3):
            return vec3(self.e * t.e)
        else: 
            return vec3(self.e * t)
    
    def __truediv__(self, t: float):
        return self * (1/t)

@njit
def dotNumba(u: np.ndarray, v: np.ndarray) -> float: 
    return np.dot(u, v)

def dot(u: vec3, v: vec3) -> float: 
    return dotNumba(u.e,v.e)

@njit
def crossNumba(u: np.ndarray, v: np.ndarray) -> float: 
    return np.linalg.cross(u, v)

def cross(u: vec3, v: vec3) -> vec3:
    cross_e = crossNumba(u.e, v.e)
    return vec3(cross_e[0], cross_e[1], cross_e[2])

@njit
def normNumba(v: np.ndarray) -> float: 
    return np.linalg.norm(v)

def unit_vector(v: vec3) -> vec3 :
    norm = normNumba(v.e)
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

@njit
def reflectNumba(v: np.ndarray, n:np.ndarray):
    return v - n*dotNumba(v,n)*2

def reflect(v: vec3, n:vec3):
    return vec3(reflectNumba(v.e,n.e))


def refract(uv: vec3, n: vec3, etai_over_etat: float):
    
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perp = (uv + n*cos_theta) * etai_over_etat
    r_out_parallel =  n * -np.sqrt(abs(1.0 - r_out_perp.length_squared()))
    return r_out_perp + r_out_parallel