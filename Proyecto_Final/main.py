from vec3_class import vec3, dot, cross, unit_vector
from color_func import write_color
from ray_class import ray
import sys
import numpy as np

'''
image_width = 256
image_height = 256
with open("image1.ppm", "w") as file:
    file.write(f'P3\n{image_width} {image_height}\n255\n')

for j in range(image_height):
    for i in range(image_width):
        pixel_color = vec3(i / (image_width-1),j / (image_height-1),0)
        write_color("image1.ppm",pixel_color)
'''

color = vec3
point3 = vec3

def hit_sphere(center: point3, radius: float, r: ray):
    oc = center - r.origin()
    a = r.direction().length_squared()
    #b = -2.0 * dot(r.direction(), oc)
    h = dot(r.direction(), oc)
    c = oc.length_squared() - radius*radius
    discriminant = h*h - a*c
    #return (discriminant >= 0)
    if (discriminant < 0):
        return -1.0
    else:
        return (h - np.sqrt(discriminant)) / a

def ray_color(r: ray):
    #if (hit_sphere(point3(0,0,-1), 0.5, r)):
    #    return color(1,0,0)
    t = hit_sphere(point3(0,0,-1), 0.5, r)
    if (t > 0.0):
        N = unit_vector(r.at(t) - vec3(0,0,-1))
        return color(N.x()+1, N.y()+1, N.z()+1)*0.5

    unit_direction = unit_vector(r.direction())
    a = 0.5*(unit_direction.y()+1.0)
    return color(1.0,1.0,1.0)*(1.0-a) + color(0.5,0.7,1.0)*a
    
def main():

    # Image

    aspect_ratio = 16.0 / 9.0
    image_width = 400

    # Calculate image height, ensure it's at least 1
    image_height = int(image_width / aspect_ratio)
    image_height = 1 if (image_height < 1) else image_height

    # Camera

    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (float(image_width)/image_height)
    camera_center = point3(0, 0, 0)

    # Calculate vectors across horizontal and down vertical viewport edges
    viewport_u = vec3(viewport_width, 0, 0)
    viewport_v = vec3(0, -viewport_height, 0)

    # Calculate horizontal and vertical delta vectores from pixel to pixel
    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    # Calculate location of upper left pixel
    viewport_upper_left = camera_center - vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2
    pixel00_loc = viewport_upper_left + (pixel_delta_u + pixel_delta_v) * 0.5

    # Render 

    with open("image7.ppm", "w") as file:
        file.write(f'P3\n{image_width} {image_height}\n255\n')

    for j in range(image_height):
        print(f'\rScanlines remaining {image_height-j} ', file=sys.stderr)
        for i in range(image_width):
            pixel_center = pixel00_loc + (pixel_delta_u * i) + (pixel_delta_v * j)
            ray_direction = pixel_center - camera_center
            r = ray(camera_center, ray_direction)

            pixel_color = ray_color(r)
            write_color("image7.ppm",pixel_color)
    
    print("\rDone.                 \n", file=sys.stderr)

main()