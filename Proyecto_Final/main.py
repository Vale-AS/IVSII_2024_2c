import time
import sys
import numpy as np
from vec3_class import vec3
from camera_class import camera
from hittable_list_class import hittable_list
from sphere_class import sphere

color = vec3
point3 = vec3

def main():

    # World

    world = hittable_list()

    world.add(sphere(point3(np.array([0,0,-1])), 0.5))      # Pelota
    world.add(sphere(point3(np.array([0,-100.5,-1])), 100)) # Piso

    cam = camera()

    cam.aspect_ratio = 16.0/9.0
    cam.image_width = 400
    cam.samples_per_pixel = 10

    cam.render(world, "carbon.ppm")


start = time.time()
main()
end = time.time()
print(f'Elapsed time: {end - start}s', file=sys.stderr)

#print=71.8208703994751
#file=88.27363443374634