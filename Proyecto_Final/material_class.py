from hittable_class import hit_record
from ray_class import ray
from vec3_class import vec3, random_unit_vector, reflect, unit_vector, dot, refract
from rtweekend import random_double
import numpy as np

color = vec3

class material:
    def scatter(r_in: ray, rec: hit_record):
        return False, None, None

class lambertian(material): 
    
    def __init__(self, albedo: color):
        self.albedo = albedo

    def scatter(self, r_in: ray, rec: hit_record):

        scatter_direction = rec.normal + random_unit_vector()
        
        #Agarrar degenerados
        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered = ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True, scattered, attenuation

class metal(material):

    def __init__(self, albedo: color, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, r_in: ray, rec: hit_record):

        reflected = reflect(r_in.direction(), rec.normal)
        reflected = unit_vector(reflected) + random_unit_vector()*self.fuzz

        scattered = ray(rec.p, reflected)
        attenuation = self.albedo
        return (dot(scattered.direction(), rec.normal) > 0), scattered, attenuation
    
class dielectric(material):

    def __init__(self, refraction_index: float):
        self.refraction_index = refraction_index
    
    def scatter(self, r_in: ray, rec: hit_record):
        attenuation = color(1.0, 1.0, 1.0)
        ri = (1.0/self.refraction_index) if rec.front_face else self.refraction_index
        
        unit_direction = unit_vector(r_in.direction())

        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = np.sqrt(1.0 - cos_theta**2)

        cannot_refract = ri * sin_theta > 1.0

        if cannot_refract or self.reflectance(cos_theta, ri) > random_double():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, ri)

        scattered = ray(rec.p, direction)
        return True, scattered, attenuation
        
    def reflectance(self, cosine: float, refraction_index):
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 *= r0
        return r0 + (1-r0)*((1-cosine)**5)