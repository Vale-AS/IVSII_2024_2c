from vec3_class import vec3, dot, cross, unit_vector
from color_func import write_color
from ray_class import ray
import sys
import numpy as np
from hittable_class import hittable, hit_record
from camera_class import camera
from hittable_list_class import hittable_list
from sphere_class import sphere
from rtweekend import infinity
from interval_class import interval

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

def main():

    # World

    world = hittable_list()

    world.add(sphere(point3(np.array([0,0,-1])), 0.5)) # Pelota
    world.add(sphere(point3(np.array([0,-100.5,-1])), 100)) # Piso

    cam = camera()

    cam.aspect_ratio = 16.0/9.0
    cam.image_width = 400

    cam.render(world, "images/image10.ppm")


main()