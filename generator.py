import os
import cv2
import math
import numpy as np
import random as rand
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageFilter

def get_color(color):
    '''Generate a color

    Args:
        color : color name string

    Returns:
        color_code: hue, saturation, luminance string
        color: color name string
    '''

    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown', 'black', 'gray', 'white']

    if not color in colors:
        color = rand.choice(colors)

    saturation = rand.randint(50, 100)
    luminance = rand.randint(40, 60)

    if color == 'red':
        hue = rand.randint(0, 4)
    elif color == 'orange':
        hue = rand.randint(9, 33)
    elif color == 'yellow':
        hue = rand.randint(43, 55)
    elif color == 'green':
        hue = rand.randint(75, 120)
    elif color == 'blue':
        hue = rand.randint(200, 233)
    elif color == 'purple':
        hue = rand.randint(266, 291)
    elif color == 'brown':
        hue = rand.randint(13, 20)
        saturation = rand.randint(25, 50)
        luminance = rand.randint(22, 40)
    elif color == 'black':
        hue = rand.randint(266, 291)
    elif color == 'gray':
        hue = rand.randint(0, 360)
        saturation = rand.randint(0, 12)
        luminance = rand.randint(25, 60)
    elif color == 'white':
        hue = rand.randint(0, 360)
        saturation = rand.randint(0, 12)
        luminance = rand.randint(80, 100)
    else:
        sys.exit('color not found')
    color_code = 'hsl(%d, %d%%, %d%%)' % (hue, saturation, luminance)

    return color_code, color

def draw_shape(shape, draw, size, color):
    '''Draw random shape

    Args:
        shape: str shape name
        draw: ImageDraw.Draw
        size: max size of target in pixels
        color: hsl color string

    Returns:
        shape: Target.shape
    '''
    shapes = ['circle', 'semicircle', 'quarter_circle', 'triangle', 'square', 'rectangle', 'trapezoid',
                'pentagon', 'hexagon', 'heptagon', 'octagon', 'star', 'cross']

    if not shape in shapes:
        shape = rand.choice(shapes)

    if shape == 'circle':
        draw_circle(draw, size, color)
    elif shape == 'semicircle':
        draw_semicircle(draw, size, color)
    elif shape == 'quarter_circle':
        draw_quarter_circle(draw, size, color)
    elif shape == 'triangle':
        draw_polygon(draw, size, 3, color)
    elif shape == 'square':
        draw_square(draw, size, color)
    elif shape == 'rectangle':
        draw_rectangle(draw, size, color)
    elif shape == 'trapezoid':
        draw_trapezoid(draw, size, color)
    elif shape == 'pentagon':
        draw_polygon(draw, size, 5, color)
    elif shape == 'hexagon':
        draw_polygon(draw, size, 6, color)
    elif shape == 'heptagon':
        draw_polygon(draw, size, 7, color)
    elif shape == 'octagon':
        draw_polygon(draw, size, 8, color)
    elif shape == 'star':
        draw_star(draw, size, color)
    elif shape == 'cross':
        draw_cross(draw, size, color)
    else:
       return None
    return shape


def draw_circle(draw, size, color):
    square_height = size[0]*70/100
    square_border = (size[0] - square_height)/2
    top=(square_border, square_border)
    bottom=(size[0]-square_border, size[0]-square_border)
    draw.pieslice([top, bottom], 0, 360, fill=color)

def draw_semicircle(draw, size, color):
    square_height = size[0]*92/100
    square_border = (size[0] - square_height)/2
    offset = square_height/4
    top=(square_border, square_border+offset)
    bottom=(size[0]-square_border, size[0]-square_border+offset)
    draw.pieslice([top, bottom], 180, 360, fill=color)

def draw_quarter_circle(draw, size, color):
    square_height = size[0]*155/100
    square_border = (size[0] - square_height)/2
    offset = square_height/4
    top=(square_border+offset, square_border+offset)
    bottom=(size[0]-square_border+offset,
            size[0]-square_border+offset)
    draw.pieslice([top, bottom], 180, 270, fill=color)
    draw.point((0,0), fill=color)
    draw.point((0,0), fill=color)

def draw_square(draw, size, color):
    square_height = size[0]*75/100
    square_border = (size[0] - square_height)/2
    top=(square_border, square_border)
    bottom=(size[0]-square_border, size[0]-square_border)
    draw.rectangle([top, bottom], fill=color)

def draw_rectangle(draw, size, color):
    rectangle_width = size[0]*55/100
    rectangle_height = size[0]*89/100

    border_width = (size[0] - rectangle_width)/2
    border_height = (size[0] - rectangle_height)/2
    top=(border_width, border_height)
    bottom=(size[0]-border_width, size[0]-border_height)
    draw.rectangle([top, bottom], fill=color)

def draw_trapezoid(draw, size, color):
    top_width = size[0]*55/100
    bottom_width = size[0]*82/100
    height = size[0]*51/100

    border_top_width = (size[0] - top_width)/2
    border_bottom_width = (size[0] - bottom_width)/2
    border_height = (size[0] - height)/2

    top_left=(border_top_width, border_height)
    top_right=(size[0]-border_top_width, border_height)

    bottom_left=(border_bottom_width,
                    size[0]-border_height)

    bottom_right=(size[0]-border_bottom_width,
                    size[0]-border_height)
    draw.polygon((top_left,
                    top_right,
                    bottom_right,
                    bottom_left),
                    fill=color)

def draw_star(draw, size, color):
    sides = 5
    cord = size[0]*55/100
    angle = 2*math.pi/sides
    rotation = math.pi/2
    points =[]
    for s in (0,2,4,1,3):
        points.append(math.cos(angle*s-rotation)*cord+size[0]/2)
        points.append(math.sin(angle*s-rotation)*cord+size[0]/2)
    draw.polygon(points, fill=color)

    #fill in the center pentagon
    rotation = math.pi*3/2
    cord = size[0]*23/100
    points =[]
    for s in range(sides):
        points.append(math.cos(angle*s-rotation)*cord+size[0]/2)
        points.append(math.sin(angle*s-rotation)*cord+size[0]/2)
    draw.polygon(points, fill=color)

def draw_polygon(draw, size, sides, color):
    cord = size[0]*47/100
    angle = 2*math.pi/sides
    rotation = 0
    points =[]
    if(sides % 2 == 1):
        rotation = math.pi/2
    for s in range(sides):
        points.append(math.cos(angle*s-rotation)*cord+size[0]/2)
        points.append(math.sin(angle*s-rotation)*cord+size[0]/2)
    draw.polygon(points, fill=color)

def draw_cross(draw, size, color):
    rectangle_width = size[0]*38/100
    rectangle_height = size[0]*92/100

    border_width = (size[0] - rectangle_width)/2
    border_height = (size[0] - rectangle_height)/2
    top=(border_width, border_height)
    bottom=(size[0]-border_width, size[0]-border_height)
    draw.rectangle([top, bottom], fill=color)
    # draw rectanle turned
    top=(border_height, border_width)
    bottom=(size[0]-border_height, size[0]-border_width)
    draw.rectangle([top, bottom], fill=color)

def draw_text(alpha, draw, size, color):
    '''Draw random alphanumeric

    Args:
        alpha: str character on target
        draw: ImageDraw.Draw
        size: max size of target in pixels
        color: hsl color string

    Returns:
        text: the alphanumeric that was drawn
    '''
    dirname, _ = os.path.split(os.path.abspath(__file__))
    font_location = os.path.join(dirname, "FreeSansBold.ttf")
    font = ImageFont.truetype(font_location, size=int(size[0]*50/100))
    text = alpha
    if not alpha in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'):
        text = rand.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    text_width, text_height = draw.textsize(text, font)
    text_pos = ((size[0]-text_width)/2, (size[1]-text_height)/2)
    draw.text(text_pos, text, fill=color, font=font)
    return text

def create_target(shape, alpha, orientation, size, shape_color_code, alpha_color_code):
    im = Image.new('RGBA', size, color=(0,0,0,0))
    draw = ImageDraw.Draw(im)
    shape = draw_shape(shape, draw, size, shape_color_code)
    text = draw_text(alpha, draw, size, alpha_color_code)
    im = ImageOps.expand(im, border=int(size[0]*10/100), fill=(0))
    if orientation >= 360 or orientation < 0:
        orientation=rand.randint(0,355)
    im = im.rotate(orientation)

    return im
