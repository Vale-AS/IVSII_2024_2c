from rtweekend import infinity

class interval:
    def __init__(self, min: float = None, max: float = None):
        if min == None and max == None:
            self.min = infinity
            self.max = -infinity
        else:
            self.min = min
            self.max = max
    
    def size(self) -> float:
        return self.max - self.min
    
    def contains(self, x: float) -> bool:
        return self.min <= x and x <= self.max
    
    def surrounds(self, x: float) -> bool:
        return self.min < x and x < self.max

    def clamp(self, x: float) -> float:
        if x < self.min: return self.min
        if x > self.max: return self.max
        return x

empty = interval(infinity, -infinity)
universe = interval(-infinity, infinity)