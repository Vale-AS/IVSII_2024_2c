from hittable_class import hittable, hit_record
from vec3_class import vec3, dot
from ray_class import ray
from interval_class import interval
from material_class import material
from math import sqrt

point3 = vec3

class sphere(hittable):

    def __init__(self, center: point3, radius: float, mat: material):
        self.center = center
        self.radius = max(0, radius)
        self.mat = mat
    
    def hit(self, r: ray, ray_t: interval):
        oc = self.center - r.origin()
        a = r.direction().length_squared()
        h = dot(r.direction(), oc)
        c = oc.length_squared() - self.radius*self.radius

        discriminant = h*h - a*c
        if (discriminant < 0):
            return False, None
        
        sqrtd = sqrt(discriminant)

        # Find nearest root that lies in acceptable range
        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return False, None
        
        info_rec = hit_record()

        info_rec.t = root
        info_rec.p = r.at(info_rec.t)
        outward_normal = (info_rec.p - self.center) / self.radius
        info_rec.set_face_normal(r, outward_normal)
        info_rec.mat = self.mat

        return True, info_rec