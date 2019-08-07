import cv2
import json
import numpy as np
from PIL import Image
from rtree import index
import matplotlib.pyplot as plt

import util, json
from target import Target

class Controller():

    def __init__(self, target_json_file, plane_json_file=None, camera_json_file=None):
        self.targets = []
        self.idx = index.Index()

        with open(target_json_file) as target_json:
            target_data = json.load(target_json)
            for i, target in enumerate(target_data):
                t = Target(target["lat"], target["lon"], target, target["size"])
                self.targets.append(t)
                diff = t.size/2
                left, bottom, right, top = (t.x - diff, t.y - diff, t.x + diff, t.y + diff)
                self.idx.insert(i, (left, bottom, right, top), obj=t)

        if plane_json_file:
            self.update_plane_json(plane_json_file)
        else:
            # Defualt Plane Telemetry
            self.x, self.y, self.z = 0.0, 0.0, 500.0
            # Default Gimbal Orientation
            self.roll, self.pitch, self.yaw = 0.0, 0.0, 0.0

        if camera_json_file:
            self.update_camera_json(camera_json_file)
        else:
            # Defualt Image resolution
            self.width, self.height = 5456, 3632
            # Default Camera Setting
            self.fov_x = 78 * np.pi / 180
            self.fov_y = np.arctan(self.height * np.tan(self.fov_x/2) / self.width) * 2

    def update_plane(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def update_plane_latlon(self, lat, lon, z=None):
        self.y, self.x = util.gps_to_feet(lat, lon)
        if z :
            self.z = z

    def update_plane_json(self, file):
        """Takes a JSON file with the attributes lat, lon, z,
        roll, pitch, yaw. Updates the plane position and orientation."""
        with open(file) as plane_json:
            plane = json.load(plane_json)
            self.update_plane_latlon(plane['lat'], plane['lon'], plane['z'])
            self.update_gimbal(plane['roll'], plane['pitch'], plane['yaw'])

    def update_gimbal(self, roll, pitch, yaw):
        self.roll, self.pitch, self.yaw = roll, pitch, yaw

    def update_camera(self, fov_x, fov_y):
        self.fov_x, self.fov_y = fov_x, fov_y

    def update_camera_json(self, file):
        """Takes a JSON files with the attributes width (in pixels),
        height (in pixels), fov_x, and fov_y."""
        with open(file) as camera_json:
            camera = json.load(camera_json)
            self.update_camera(camera['fov_x'], camera['fov_y'])
            self.height = camera['height']
            self.width = camera['width']

    def generate_image(self, points, color=(0, 255, 0, 255)):
        left, bottom, right, top = util.get_bouding_box(points)

        targets = list(self.idx.intersection((left, bottom, right, top), objects="raw"))
        if len(targets) == 0:

            img = Image.new('RGBA', (self.width, self.height), color)
            return img, False

        targets = sorted(targets)
        width, height = right - left, top - bottom
        points[:,0] -= left
        points[:,1] -= bottom
        scaling_factor = self.width / width
        target_size = int(scaling_factor)
        #print(scaling_factor)
        width *= scaling_factor
        height *= scaling_factor
        points*= scaling_factor
        img = Image.new('RGBA', (int(width), int(height)), color)
        for t in targets:
            offset = (int((t.x - left)*scaling_factor), int((t.y - bottom)*scaling_factor))
            target_img = t.create(target_size * t.size, target_size * t.size)
            img = util.compose(img, target_img, offset)

        return np.asarray(img), True

    def capture(self):
        ground_pts = util.get_points(self.x, self.y, self.z,
                                     self.roll, self.pitch, self.yaw,
                                     self.fov_x, self.fov_y)
        #print(ground_pts)
        im, flag = self.generate_image(ground_pts)
        #print(ground_pts)
        #plt.imshow(im)
        #plt.plot(ground_pts[:,0], ground_pts[:,1], "-")
        #plt.plot(ground_pts[0,0], ground_pts[0,1], "ro")

        #plt.plot(ground_pts[3,0], ground_pts[3,1], "go")
        #plt.show()

        if flag:
            image_pts = np.array([[self.width, 0],
                                  [self.width, self.height],
                                  [0, self.height],
                                  [0,0]])

            h, status = cv2.findHomography(ground_pts, image_pts)
            im2 = cv2.warpPerspective(im, h, (self.width, self.height))
            plt.imshow(im2)
            plt.show()
            return im2

        return im

if __name__ == "__main__":
    c = Controller("json/data.json", plane_json_file="json/plane.json", camera_json_file="json/firstpass.json")
    arr = c.capture()
    im = Image.fromarray(arr)
    im.save('figures/firstpass.png')
    c.update_camera_json('json/secondpass.json')
    arr = c.capture()
    im = Image.fromarray(arr)
    im.save('figures/secondpass.png')
