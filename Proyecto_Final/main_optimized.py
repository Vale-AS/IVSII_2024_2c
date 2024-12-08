import time
import sys
import os
import numpy as np
from vec3_class import vec3, random
from camera_class_optimized import camera
from hittable_list_class import hittable_list
from sphere_class import sphere
from material_class import material, lambertian, metal, dielectric
from rtweekend import pi, random_double
from multiprocessing import Pool

color = vec3
point3 = vec3

def main():

    # World

    world = hittable_list()

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

    cores = 8
    
    p = Pool(cores)
    line_ammount = 400 / 16.0 * 9.0

    args = []

    for c in range(cores):
        interval = range(int(c*line_ammount/cores), int((c+1)*line_ammount/cores))
        args.append((world, interval, f"bolas-fest-{c+1}.ppm"))

    p.map(cam.render, args)

    # Concateno los archivos
    with open("mega_bolas_fest.ppm", "w") as file:
        file.write(f'P3\n{400} {int(line_ammount)}\n255\n')
    
        # Unificar los archivos
        for c in range(cores):
            file_name = f"bolas-fest-{c+1}.ppm"

            with open(file_name, "r") as f:
                data = f.readlines()[3:]
                for line in data:
                    file.write(line)

start = time.time()
main()
end = time.time()
print(f'Elapsed time: {end - start}s', file=sys.stderr)