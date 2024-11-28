from vec3_class import vec3
point3 = vec3

class ray:
    
    def __init__(self):
        pass

    def __init__(self, origin: point3, direction: vec3):
        self.orig = origin
        self.dir = direction
    
    def origin(self): return self.orig
    def direction(self): return self.dir

    def at(self, t: float) -> point3:
        return self.orig + self.dir * t