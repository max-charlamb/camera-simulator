import json, random, util

shapes = ['circle', 'semicircle', 'quarter_circle', 'triangle', 'square', 'rectangle', 'trapezoid',
                'pentagon', 'hexagon', 'heptagon', 'octagon', 'star', 'cross']
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'black', 'gray', 'white']
alphas = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0']

def createShape(shape, alpha, shape_color, alpha_color, orientation, lat, lon, size):
    return {
    		"shape" : shape,
            "alpha" : alpha,
            "shape_color" : shape_color,
            "alpha_color" : alpha_color,
            "orientation" : orientation,
            "y": lat,
            "x": lon,
            "size": size
           }

def createRandomShape():
    alpha_color, shape_color = (None, None)
    while alpha_color == shape_color:
        shape_color = random.choice(colors)
        alpha_color = random.choice(colors)
    x = random.randint(0, 40)
    y = random.randint(0, 40)
    return {
    		"shape" : random.choice(shapes),
            "alpha" : random.choice(alphas),
            "shape_color" : shape_color,
            "alpha_color" : alpha_color,
            "orientation" : random.randint(0, 359),
            "y": y,
            "x": x,
            "lat" : util.feet_to_gps(y),
            "lon" : util.feet_to_gps(x),
            "size": random.randint(1, 5)
           }

def createShapes(n):
    shapes = []
    while n > 0:
        shapes.append(createRandomShape())
    return shapes



if __name__ == "__main__":
    data = []
    data.append(createRandomShape())
    data.append(createRandomShape())
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
