import time
import sys
import os
import numpy as np
from vec3_class import vec3
from camera_class import camera
from hittable_list_class import hittable_list
from sphere_class import sphere
from material_class import material, lambertian, metal

color = vec3
point3 = vec3

def main():

    # World

    world = hittable_list()

    #world.add(sphere(point3(np.array([0,0,-1])), 0.5))      # Pelota
    #world.add(sphere(point3(np.array([0,-100.5,-1])), 100)) # Piso
    
    material_ground = lambertian(color(np.array([0.8, 0.8, 0.0])))
    material_center = lambertian(color(np.array([0.1, 0.2, 0.5])))
    material_left   = metal(color(np.array([0.8, 0.8, 0.8])), 0.3)
    material_right  = metal(color(np.array([0.8, 0.6, 0.2])), 1.0)

    world.add(sphere(point3(np.array([ 0.0, -100.5, -1.0])), 100.0, material_ground))
    world.add(sphere(point3(np.array([ 0.0,    0.0, -1.2])),   0.5, material_center))
    world.add(sphere(point3(np.array([-1.0,    0.0, -1.0])),   0.5, material_left))
    world.add(sphere(point3(np.array([ 1.0,    0.0, -1.0])),   0.5, material_right))

    cam = camera()

    cam.aspect_ratio = 16.0/9.0
    cam.image_width = 400
    cam.samples_per_pixel = 10
    cam.max_depth = 10

    cam.render(world, "bolas-fest.ppm")


start = time.time()
main()
end = time.time()
print(f'Elapsed time: {end - start}s', file=sys.stderr)