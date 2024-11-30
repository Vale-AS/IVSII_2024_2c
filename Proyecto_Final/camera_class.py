from vec3_class import vec3, dot, cross, unit_vector
from color_func import write_color
from ray_class import ray
import sys
import numpy as np
from hittable_class import hittable, hit_record
from hittable_list_class import hittable_list
from sphere_class import sphere
from rtweekend import infinity, random_double
from interval_class import interval

color = vec3
point3 = vec3

class camera:
    
    # Image
    aspect_ratio = 1.0
    image_width = 100
    samples_per_pixel = 10

    def initialize(self):

        # Calculate image height, ensure it's at least 1
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = 1 if (self.image_height < 1) else self.image_height
        self.pixel_samples_scale = 1.0 / self.samples_per_pixel

        
        # Camera
        focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (float(self.image_width)/self.image_height)
        self.center = point3(np.array([0, 0, 0]))

        # Calculate vectors across horizontal and down vertical viewport edges
        viewport_u = vec3(np.array([viewport_width, 0, 0]))
        viewport_v = vec3(np.array([0, -viewport_height, 0]))

        # Calculate horizontal and vertical delta vectores from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate location of upper left pixel
        viewport_upper_left = self.center - vec3(np.array([0, 0, focal_length])) - viewport_u/2 - viewport_v/2
        self.pixel00_loc = viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) * 0.5

    def get_ray(self, i:int, j:int) -> ray:
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + (self.pixel_delta_u * (i + offset.x())) + (self.pixel_delta_v * (j + offset.y()))
        
        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin
        return ray(ray_origin, ray_direction)
    
    def sample_square(self) -> vec3:
        return vec3(np.array([random_double() - 0.5, random_double() - 0.5, 0.0]))

    def ray_color(self, r: ray, world: hittable) -> color:
        does_hit, info_rec = world.hit(r, interval(0, infinity))
        if does_hit:
            return (info_rec.normal + color(np.array([1,1,1]))) * 0.5

        unit_direction = unit_vector(r.direction())
        a = 0.5*(unit_direction.y()+1.0)
        return color(np.array([1.0,1.0,1.0]))*(1.0-a) + color(np.array([0.5,0.7,1.0]))*a
        

    def render(self, world: hittable, file_name: str):

        self.initialize()

        with open(file_name, "w") as file:
            file.write(f'P3\n{self.image_width} {self.image_height}\n255\n')

        for j in range(self.image_height):
            print(f'\rScanlines remaining {self.image_height-j} ', file=sys.stderr)
            for i in range(self.image_width):

                # pixel_center = self.pixel00_loc + (self.pixel_delta_u * i) + (self.pixel_delta_v * j)
                # ray_direction = pixel_center - self.center
                # r = ray(self.center, ray_direction)

                # pixel_color = self.ray_color(r, world)
                # write_color(file_name,pixel_color)
                
                pixel_color = color(np.array([0,0,0]))
                for sample in range(self.samples_per_pixel):
                    r = self.get_ray(i, j)
                    pixel_color = pixel_color + self.ray_color(r, world)
                write_color(file_name, pixel_color*self.pixel_samples_scale)
        
        print("\rDone.                 \n", file=sys.stderr)       