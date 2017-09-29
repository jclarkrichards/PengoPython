import numpy as np
from vectors import Vector2D

#Unit width and height in pixels
WIDTH = 16
HEIGHT = 16

#Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (55, 55, 55)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (127, 0, 255)
ORANGE = (255, 128, 0)
TEAL = (0, 255, 255)

#Directions to move (Never moves straight up or diagonally down)
RIGHT = Vector2D(1, 0)
LEFT = Vector2D(-1, 0)
UPRIGHT = Vector2D(1, -1)
UPLEFT = Vector2D(-1, -1)
DOWN = Vector2D(0, 1)

NROWS, NCOLS = 20, 32
#NROWS, NCOLS = 10, 16 #Small Test Screen
COLUMNOFFSET = 0

A = np.zeros((NROWS, NCOLS))
A[:, 0] = 1
A[:, -1] = 1
A[-1, :] = 1
              
#LEFTEDGE, RIGHTEDGE = 0, 9 #playfield is 10 units wide
SCREENSIZE = ((NCOLS)*WIDTH, NROWS*HEIGHT)
