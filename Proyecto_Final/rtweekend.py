import random

# Constants
infinity = float('inf')
pi = 3.1415926535897932385

# Utility Functions 

def degrees_to_radians(degrees: float) -> float:
    return degrees * pi / 180.0

def random_double(min: float = 0, max: float = 1):
    return random.uniform(min, max)