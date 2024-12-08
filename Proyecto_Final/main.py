import time
import sys
import os
import numpy as np
from vec3_class import vec3, random
from camera_class import camera
from hittable_list_class import hittable_list
from sphere_class import sphere
from material_class import lambertian, metal, dielectric
from rtweekend import random_double

color = vec3
point3 = vec3

def main():

    # World

    world = hittable_list()

    # world.add(sphere(point3(np.array([0,0,-1])), 0.5))      # Pelota
    # world.add(sphere(point3(np.array([0,-100.5,-1])), 100)) # Piso
    # material_left   = metal(color(np.array([0.8, 0.8, 0.8])), 0.3)
    
    # material_ground = lambertian(color(0.8, 0.8, 0.0))
    # material_center = lambertian(color(0.1, 0.2, 0.5))
    # material_left   = dielectric(1.50)
    # material_bubble = dielectric(1.00/1.50)
    # material_right  = metal(color(0.8, 0.6, 0.2), 1.0)
# 
    # world.add(sphere(point3( 0.0, -100.5, -1.0), 100.0, material_ground))
    # world.add(sphere(point3( 0.0,    0.0, -1.2),   0.5, material_center))
    # world.add(sphere(point3(-1.0,    0.0, -1.0),   0.5, material_left))
    # world.add(sphere(point3(-1.0,    0.0, -1.0),   0.4, material_bubble))
    # world.add(sphere(point3( 1.0,    0.0, -1.0),   0.5, material_right))

    # R = np.cos(pi/4)
    # 
    # material_left = lambertian(color(np.array([0,0,1])))
    # material_right = lambertian(color(np.array([1,0,0])))
# 
    # world.add(sphere(point3(np.array([-R, 0, -1])), R, material_left))
    # world.add(sphere(point3(np.array([ R, 0, -1])), R, material_right))

    # cam = camera()
# 
    # cam.aspect_ratio = 16.0/9.0
    # cam.image_width = 400
    # cam.samples_per_pixel = 10
    # cam.max_depth = 10
# 
    # cam.vfov = 20
    # cam.lookfrom = point3(-2.0,2.0,1.0)
    # cam.lookat   = point3(0.0,0.0,-1.0)
    # cam.vup      = vec3(0.0,1.0,0.0)
# 
    # cam.defocus_angle = 10.0
    # cam.focus_dist    = 3.4
# 
    # cam.render(world, "raytraced-image-test.ppm")


    # Final render
    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(sphere(point3(0.0,-1000.0,0.0), 1000.0, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random_double()
            center = point3(a + 0.9*random_double(), 0.2, b + 0.9*random_double())

            if ((center - point3(4, 0.2, 0)).length() > 0.9):
            
                if (choose_mat < 0.8):
                    # diffuse
                    albedo = random() * random()
                    sphere_material = lambertian(albedo)
                    world.add(sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = random(0.5, 1)
                    fuzz = random_double(0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = dielectric(1.5)
                    world.add(sphere(center, 0.2, sphere_material))
                
    material1 = dielectric(1.5)
    world.add(sphere(point3(0, 1, 0), 1.0, material1))

    material2 = lambertian(color(0.4, 0.2, 0.1))
    world.add(sphere(point3(-4, 1, 0), 1.0, material2))

    material3 = metal(color(0.7, 0.6, 0.5), 0.0)
    world.add(sphere(point3(4, 1, 0), 1.0, material3))

    cam = camera()

    cam.aspect_ratio      = 16.0 / 9.0
    cam.image_width       = 400
    cam.samples_per_pixel = 10
    cam.max_depth         = 5

    cam.vfov     = 20
    cam.lookfrom = point3(13.0,2.0,3.0)
    cam.lookat   = point3(0.0,0.0,0.0)
    cam.vup      = vec3(0.0,1.0,0.0)

    cam.defocus_angle = 0.6
    cam.focus_dist    = 10.0

    cam.render(world, "raytraced_image.ppm")


start = time.time()
main()
end = time.time()
print(f'Elapsed time: {end - start}s', file=sys.stderr)