from vec3_class import vec3 as color
from interval_class import interval

def write_color(filename: str, pixel_color: color):
    r = pixel_color.x()
    g = pixel_color.y()
    b = pixel_color.z()

    intensity = interval(0.000, 0.999)
    rbyte = int(255.999 * intensity.clamp(r))
    gbyte = int(255.999 * intensity.clamp(g))
    bbyte = int(255.999 * intensity.clamp(b))

    if filename:
        with open(filename, 'a') as f:
            f.write(f'{rbyte} {gbyte} {bbyte}\n')
    else:
        print(f'{rbyte} {gbyte} {bbyte}\n')