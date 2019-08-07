import cv2 
import math
import numpy as np
import matplotlib.pyplot as plt


width, height = 800, 400

fov_x = 78 * np.pi / 180
fov_y = np.arctan(height * np.tan(fov_x/2) / width) * 2

roll, pitch, yaw = -20.0 * np.pi / 180, 10.0 * np.pi / 180, 30.0 * np.pi / 180

x, y, z = 700.0, 400.0, 300.0

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
	theta = np.asarray([roll, pitch, yaw])
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

	return (min_x, max_y, max_x, min_y)

im = cv2.imread("test.jpg")

print(im.shape)


pts = get_points(x, y, z, roll, pitch, yaw, fov_x, fov_y)
print(pts)
pts2 = np.array([[width,0],[width,height], [0,height], [0,0]]) 

plt.imshow(im)
plt.plot(pts[:,0], pts[:,1], "-")
plt.plot(pts[0,0], pts[0,1], "ro")

plt.plot(pts[3,0], pts[3,1], "go")
plt.show()
h, status = cv2.findHomography(pts, pts2)

im2 = cv2.warpPerspective(im, h, (width, height))
plt.imshow(im2)
plt.show() 