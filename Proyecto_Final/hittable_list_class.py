from hittable_class import hittable, hit_record
from ray_class import ray
from interval_class import interval

class hittable_list(hittable):
    objects = []

    
    def __init__(self, *, object: hittable = None):
        if object == None:
            self.objects = []
        else:
            self.objects = []
            self.add(object)
    
    def clear(self):
        self.objects = []
    
    def add(self, object: hittable):
        self.objects.append(object)
    
    def hit(self, r: ray, ray_t: interval) -> bool:
        hit_anything = False
        closest_so_far = ray_t.max

        true_rec  = hit_record()
        for object in self.objects:
            does_hit, info_rec = object.hit(r, interval(ray_t.min, closest_so_far))
            if does_hit:
                hit_anything = True
                closest_so_far = info_rec.t
                true_rec = info_rec

        
        return hit_anything, true_rec