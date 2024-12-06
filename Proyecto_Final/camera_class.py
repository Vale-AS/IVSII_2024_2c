from vec3_class import vec3, dot, cross, unit_vector, random_on_hemisphere, random_unit_vector
from color_func import write_color
from ray_class import ray
import sys
import numpy as np
from hittable_class import hittable, hit_record
from hittable_list_class import hittable_list
from sphere_class import sphere
from rtweekend import infinity, random_double, degrees_to_radians
from interval_class import interval
from material_class import material

color = vec3
point3 = vec3

class camera:
    
    # Image
    aspect_ratio = 1.0
    image_width = 100
    samples_per_pixel = 10
    max_depth = 10

    vfov = 90
    lookfrom = point3(np.array([0,0,0]))
    lookat = point3(np.array([0,0,-1]))
    vup = vec3(np.array([0,1,0]))

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
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * (float(self.image_width)/self.image_height)
        #self.center = point3(np.array([0, 0, 0]))

        # Calculate the w,u,v unit basis vectors for the camera coordinate frame
        w = unit_vector(self.lookfrom - self.lookat)
        u = unit_vector(cross(self.vup, w))
        v = cross(w, u)
        
        # Calculate vectors across horizontal and down vertical viewport edges
        #viewport_u = vec3(np.array([viewport_width, 0, 0]))
        #viewport_v = vec3(np.array([0, -viewport_height, 0]))

        viewport_u = u*viewport_width
        viewport_v = -v*viewport_height
        
        # Calculate horizontal and vertical delta vectores from pixel to pixel
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate location of upper left pixel
        viewport_upper_left = self.center - (w*focal_length) - viewport_u/2 - viewport_v/2
        self.pixel00_loc = viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) * 0.5

    def get_ray(self, i:int, j:int) -> ray:
        offset = self.sample_square()
        pixel_sample = self.pixel00_loc + (self.pixel_delta_u * (i + offset.x())) + (self.pixel_delta_v * (j + offset.y()))
        
        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin
        return ray(ray_origin, ray_direction)
    
    def sample_square(self) -> vec3:
        return vec3(np.array([random_double() - 0.5, random_double() - 0.5, 0.0]))

    def ray_color(self, r: ray, depth: int, world: hittable) -> color:
        if depth <= 0:
            return color(np.array([0,0,0]))

        does_hit, info_rec = world.hit(r, interval(0.001, infinity))
        if does_hit:
            has_material, scattered, attenuation = info_rec.mat.scatter(r, info_rec)
            if has_material:
                return self.ray_color(scattered, depth-1, world) * attenuation
            return color(np.array([0,0,0]))
            # direction = info_rec.normal + random_unit_vector()
            #return self.ray_color(ray(info_rec.p, direction), depth-1, world) * 0.5

        unit_direction = unit_vector(r.direction())
        a = 0.5*(unit_direction.y()+1.0)
        return color(np.array([1.0,1.0,1.0]))*(1.0-a) + color(np.array([0.5,0.7,1.0]))*a
        

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
                
                pixel_color = color(np.array([0,0,0]))
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