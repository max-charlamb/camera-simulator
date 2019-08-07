import json
import generator
import matplotlib.pyplot as plt
import util

class Target():
    def __init__(self, lat, lon, param, size):
        self.y, self.x = util.gps_to_feet(lat,lon)
        self.lat = lat
        self.lon = lon
        self.size = size
        self.param = param
        self.target_img = None
        self.shape_color_code = None
        self.alpha_color_code = None
        self.set_color()

    def set_color(self):
        self.shape_color_code, shape_color = generator.get_color(self.param["shape_color"])
        self.text_color_code, text_color = generator.get_color(self.param["alpha_color"])
        #Prevent target and letter from being the same color
        while shape_color == text_color:
            shape_color_code, shape_color = generator.get_color()
            text_color_code, text_color = generator.get_color()

    def create(self, width, height):
        if self.target_img is None:
            self.target_img = generator.create_target(shape=self.param["shape"],
                                            alpha=self.param["alpha"],
                                            orientation=self.param["orientation"],
                                            size=(width, height),
                                            shape_color_code=self.shape_color_code,
                                            alpha_color_code=self.alpha_color_code)
        return self.target_img

    def _show(self):
        assert not self.target_img is None
        plt.imshow(self.target_img)
        plt.show()


    def __lt__(t1, t2):
        return t1.size < t2.size

    def __gt__(t1, t2):
        return t1.size > t2.size





if __name__ == "__main__":

    with open("json/data.json") as target_json:
        targets = json.load(target_json)
        for target in targets:
            t = Target(target["lat"], target["lon"], target, target["size"])
            t.create(100, 100)
            t._show()

# 10,000/90 * 3280.4
