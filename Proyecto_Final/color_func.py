from vec3_class import vec3 as color

def write_color(filename: str, pixel_color: color):
    r = pixel_color.x()
    g = pixel_color.y()
    b = pixel_color.z()

    rbyte = int(255.999 * r)
    gbyte = int(255.999 * g)
    bbyte = int(255.999 * b)

    with open(filename, 'a') as f:
        f.write(f'{rbyte} {gbyte} {bbyte}\n')