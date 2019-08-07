import json
import generator
import matplotlib.pyplot as plt

class Target():
    def __init__(self, lat, lon, param, size):
        self.lat = lat
        self.lon = lon
        self.size = size
        self.param = param
        self.target_img = None

    def create(self, width, height):
        if self.target_img is None:
            self.target_img = generator.create_target(shape=self.param["shape"],
                                            alpha=self.param["alpha"],
                                            shape_color=self.param["shape_color"],
                                            alpha_color=self.param["alpha_color"],
                                            orientation=self.param["orientation"],
                                            size=(width, height))
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

    with open("targets.json") as target_json:
        targets = json.load(target_json)
        for target in targets:
            t = Target(target["lat"], target["lon"], target, (200, 200))
            t._show()


# 10,000/90 * 3280.4