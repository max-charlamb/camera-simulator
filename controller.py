import cv2
import json
import numpy as np
from PIL import Image
from rtree import index
import matplotlib.pyplot as plt

import util
from target import Target

class Controller():

    def __init__(self, json_file):
        self.targets = []
        self.idx = index.Index()

        with open(json_file) as target_json:
            target_data = json.load(target_json)
            for i, target in enumerate(target_data):
                t = Target(target["y"], target["x"], target, target["size"])
                self.targets.append(t)
                diff = t.size/2
                left, bottom, right, top = (t.x - diff, t.y - diff, t.x + diff, t.y + diff)
                self.idx.insert(i, (left, bottom, right, top), obj=t)

        # Plane Telemetry
        self.x, self.y, self.z = 0.0, 0.0, 500.0

        # Gimbal Orientation
        self.roll, self.pitch, self.yaw = 0.0, 0.0, 0.0

        # Image resolution
        self.width, self.height = 5456, 3632

        # Camera Setting
        self.fov_x = 78 * np.pi / 180
        self.fov_y = np.arctan(self.height * np.tan(self.fov_x/2) / self.width) * 2

    def update_plane(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def update_plane_latlon(self, lat, lon, z=None):
        self.y, self.x = util.gps_to_feet(lat, lon)
        if z :
            self.z = z

    def update_gimbal(self, roll, pitch, yaw):
        self.roll, self.pitch, self.yaw = roll, pitch, yaw

    def update_camera(self, fov_x, fov_y):
        self.fov_x, self.fov_y = fov_x, fov_y

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
        print(scaling_factor)
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
        print(ground_pts)
        im, flag = self.generate_image(ground_pts)
        print(ground_pts)
        plt.imshow(im)
        plt.plot(ground_pts[:,0], ground_pts[:,1], "-")
        plt.plot(ground_pts[0,0], ground_pts[0,1], "ro")

        plt.plot(ground_pts[3,0], ground_pts[3,1], "go")
        plt.show()

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
    c = Controller("data.json")
    c.capture()
