from vec3_class import vec3, cross, unit_vector, random_in_unit_disk
from color_func import write_color
from ray_class import ray
import sys
import numpy as np
from hittable_class import hittable
from rtweekend import infinity, random_double, degrees_to_radians
from interval_class import interval

color = vec3
point3 = vec3

class camera:
    
    # Image
    aspect_ratio = 1.0
    image_width = 100
    samples_per_pixel = 10
    max_depth = 10

    vfov = 90
    lookfrom = point3(0,0,0)
    lookat = point3(0,0,-1)
    vup = vec3(0,1,0)

    defocus_angle = 0
    focus_dist = 10

    def initialize(self):

        # Calculate image height, ensure it's at least 1
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = 1 if (self.image_height < 1) else self.image_height
        self.pixel_samples_scale = 1.0 / self.samples_per_pixel

        self.center = self.lookfrom

        # Camera
        focal_length = (self.lookfrom - self.lookat).length()
        theta = degrees_to_radians(self.vfov)
        h = np.tan(theta/2)
        viewport_height = 2 * h * self.focus_dist
        viewport_width = viewport_height * (float(self.image_width)/self.image_height)
        
        # Calculate the w,u,v unit basis vectors for the camera coordinate frame
        w = unit_vector(self.lookfrom - self.lookat)
        u = unit_vector(cross(self.vup, w))
        v = cross(w, u)
        
        # Calculate vectors across horizontal and down vertical viewport edges
        viewport_u = u*viewport_width
        viewport_v = -v*viewport_height
        
        # Calculate horizontal and vertical delta vectores from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate location of upper left pixel
        viewport_upper_left = self.center - (w*self.focus_dist) - viewport_u/2 - viewport_v/2
        self.pixel00_loc = viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) * 0.5

        defocus_radius = self.focus_dist * np.tan(degrees_to_radians(self.defocus_angle / 2))
        self.defocus_disk_u = u * defocus_radius
        self.defocus_disk_v = v * defocus_radius


    def get_ray(self, i:int, j:int) -> ray:
        # Construct a camera ray originating from the defocus disk and directed at a randomly
        # sampled point around the pixel location i, j.

        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + (self.pixel_delta_u * (i + offset.x())) + (self.pixel_delta_v * (j + offset.y()))
        
        ray_origin = self.center if (self.defocus_angle <= 0) else self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin
        return ray(ray_origin, ray_direction)
    
    def sample_square(self) -> vec3:
        return vec3(random_double() - 0.5, random_double() - 0.5, 0.0)
    
    def defocus_disk_sample(self) -> point3:
        # Returns a random point in the camera defocus disk.
        p = random_in_unit_disk()
        return self.center + (self.defocus_disk_u * p[0]) + (self.defocus_disk_v * p[1])

    def ray_color(self, r: ray, depth: int, world: hittable) -> color:
        if depth <= 0:
            return color(0,0,0)

        does_hit, info_rec = world.hit(r, interval(0.001, infinity))
        if does_hit:
            has_material, scattered, attenuation = info_rec.mat.scatter(r, info_rec)
            if has_material:
                return self.ray_color(scattered, depth-1, world) * attenuation
            return color(0,0,0)

        unit_direction = unit_vector(r.direction())
        a = 0.5*(unit_direction.y()+1.0)
        return color(1.0,1.0,1.0)*(1.0-a) + color(0.5,0.7,1.0)*a
        

    def render(self, world: hittable, filename: str = None):

        self.initialize()

        if filename:
            with open(filename, "w") as file:
                file.write(f'P3\n{self.image_width} {self.image_height}\n255\n')
        else:
            print(f'P3\n{self.image_width} {self.image_height}\n255\n')

        loading = hearts

        for j in range(self.image_height):
            print(f'\rScanlines remaining {self.image_height-j}   {loading[j%(len(loading))]}', file=sys.stderr)
            print ("\033[A\033[A", file=sys.stderr) 
            for i in range(self.image_width):
                
                pixel_color = color(0,0,0)
                for sample in range(self.samples_per_pixel):
                    r = self.get_ray(i, j)
                    pixel_color = pixel_color + self.ray_color(r, self.max_depth, world)
                write_color(filename, pixel_color*self.pixel_samples_scale)
        
        print("\rDone                           :-)\n", file=sys.stderr)


zigzag = [
    "<3      ",
    " <3     ",
    "  <3    ",
    "   <3   ",
    "    <3  ",
    "     <3 ",
    "      <3",
    "     <3 ",
    "    <3  ",
    "   <3   ",
    "  <3    ",
    " <3     ",
]

hearts = [
    "3           ",
    "<3          ",
    "3<3         ",
    "<3<3        ",
    "3<3<3       ",
    "<3<3<3      ",
    " <3<3<3     ",
    "  <3<3<3    ",
    "   <3<3<    ",
    "    <3<3    ",
    "     <3<    ",
    "      <3    "
    "       <    "
]

snake = [   "⠋",
			"⠙",
			"⠸",
			"⠴",
			"⠦",
			"⠇"]

dots = [
			".       ",
			"..      ",
			"...     ",
            "....    ",
			".....   ",
			" ....   ",
			"  ...   ",
			"   ..   ",
			"    .   "]
            
bar = [
			"[    ]",
			"[=   ]",
			"[==  ]",
			"[=== ]",
			"[====]",
			"[ ===]",
			"[  ==]",
			"[   =]",
			"[    ]",
			"[   =]",
			"[  ==]",
			"[ ===]",
			"[====]",
			"[=== ]",
			"[==  ]",
			"[=   ]"]