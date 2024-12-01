from hittable_class import hittable, hit_record
from ray_class import ray
from vec3_class import vec3, random_unit_vector, reflect

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

    def __init__(self, albedo: color):
        self.albedo = albedo

    def scatter(self, r_in: ray, rec: hit_record):

        reflected = reflect(r_in.direction(), rec.normal)

        scattered = ray(rec.p, reflected)
        attenuation = self.albedo
        return True, scattered, attenuation