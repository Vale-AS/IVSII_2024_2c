import time
import sys
import os
from vec3_class import vec3, random
from camera_class_optimized import camera
from hittable_list_class import hittable_list
from sphere_class import sphere
from material_class import lambertian, metal, dielectric
from rtweekend import random_double
from multiprocessing import Pool

color = vec3
point3 = vec3

# Definimos el nombre del archivo final y la cantidad de cores a usar

if len(sys.argv)>1:
    file_name = sys.argv[1]
else:
    file_name = "raytraced_image.ppm"

if len(sys.argv)>2 and int(sys.argv[2]) in range(1,16):
    cores = int(sys.argv[2])
else:
    cores = 8

def main():

    # World

    world = hittable_list()

    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(sphere(point3(0.0,-1000.0,0.0), 1000.0, ground_material))

    #for a in range(-11, 11):
    #    for b in range(-11, 11):
    #        choose_mat = random_double()
    #        center = point3(a + 0.9*random_double(), 0.2, b + 0.9*random_double())
    #        if ((center - point3(4, 0.2, 0)).length() > 0.9):
    #        
    #            if (choose_mat < 0.8):
    #                # diffuse
    #                albedo = random() * random()
    #                sphere_material = lambertian(albedo)
    #                world.add(sphere(center, 0.2, sphere_material))
    #            elif choose_mat < 0.95:
    #                # metal
    #                albedo = random(0.5, 1)
    #                fuzz = random_double(0, 0.5)
    #                sphere_material = metal(albedo, fuzz)
    #                world.add(sphere(center, 0.2, sphere_material))
    #            else:
    #                # glass
    #                sphere_material = dielectric(1.5)
    #                world.add(sphere(center, 0.2, sphere_material))
    #            
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
    
    height = 400 / 16.0 * 9.0

    args = []

    # Genero los argumentos para cada core
    for c in range(cores):
        file_path = f"./tmp/image-piece-{c+1}.txt"
        if os.path.isfile(file_path):
            os.remove(file_path)

        interval = range(int(c*height/cores), int((c+1)*height/cores))
        args.append((world, interval, file_path, c))

    # Renderizo la escena usando todos los cores
    p = Pool(cores)
    print("Remaining lines from each process:")
    p.map(cam.render, args)
    p.close()

    if os.path.isfile(file_name):
        os.remove(file_name)

    #Concateno los archivos
    with open(file_name, "w") as file:
        file.write(f'P3\n{cam.image_width} {int(height)}\n255\n')

        for c in range(cores):
            file_path = f"./tmp/image-piece-{c+1}.txt"
            with open(file_path, "r") as f:
                data = f.readlines()
                for line in data:
                    file.write(line)
            os.remove(file_path)

start = time.time()
main()
end = time.time()
print(f'Elapsed time: {end - start}s', file=sys.stderr)