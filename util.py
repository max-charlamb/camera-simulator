import math
import numpy as np

def gps_to_feet(lat, lon):
    scaling_factor = 10000 / 90 * 3280.4
    return (scaling_factor * lat, scaling_factor * lon)

def feet_to_gps(feet):
    scaling_factor = (90 / 10000) / 3280.4
    return scaling_factor * feet

# Calculates Rotation Matrix given euler angles.
def eulerAnglesToRotationMatrix(theta) :

    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])

    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])

    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])

    R = np.dot(np.dot(R_z, R_x), R_y)
    return R

def get_points(x, y, z, roll, pitch, yaw, fov_x, fov_y):
    points = []
    theta = np.asarray([pitch, roll, yaw])
    pos = np.array([x,y,z])
    R = eulerAnglesToRotationMatrix(theta)
    v_init = np.array([0,0,-1])
    for i in [[1,-1], [1,1], [-1,1], [-1,-1]]:
        t = [i[0]*np.tan(fov_x/2), i[1]*np.tan(fov_y/2) , 0]
        v_f = R.dot(v_init + t)
        v_f = v_f / np.linalg.norm(v_f)
        point = (-pos[2]/v_f[2] * v_f)[:2] + pos[:2]
        points.append(point)
    return np.asarray(points)

def get_bouding_box(pts):
    min_x = min(pts[:,0])
    min_y = min(pts[:,1])
    max_x = max(pts[:,0])
    max_y = max(pts[:,1])
    return (min_x, min_y, max_x, max_y)

def compose(background, img, offset):
    background.paste(img, offset, img)
    return background
