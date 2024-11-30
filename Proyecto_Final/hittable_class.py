from vec3_class import vec3, dot
from ray_class import ray

class hit_record:
    def set_face_normal(self, r: ray, outward_normal: vec3):
        self.front_face = (dot(r.direction(), outward_normal) < 0)
        self.normal = outward_normal if self.front_face else -outward_normal

class hittable:
    def hit(self, r: ray, ray_tmin: float, ray_tmax: float) -> tuple[bool, hit_record]:
        return 0