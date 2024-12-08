from vec3_class import vec3 as color
from interval_class import interval
import numpy as np

def linear_to_gamma(linear_component: float) -> float:
    if linear_component > 0:
        return np.sqrt(linear_component)
    
    return 0

def write_color(filename: str, pixel_color: color):
    r = linear_to_gamma(pixel_color.x())
    g = linear_to_gamma(pixel_color.y())
    b = linear_to_gamma(pixel_color.z())

    intensity = interval(0.000, 0.999)
    rbyte = int(255.999 * intensity.clamp(r))
    gbyte = int(255.999 * intensity.clamp(g))
    bbyte = int(255.999 * intensity.clamp(b))

    with open(filename, 'a') as f:
        f.write(f'{rbyte} {gbyte} {bbyte}\n')