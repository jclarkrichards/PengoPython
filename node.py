import pygame
from constants import *
from vectors import Vector2D

class Node(object):
    def __init__(self, x, y, first=False):
        '''x and y are in array units'''
        self.first = first
        self.position = Vector2D(x, y)
        self.nextNode = self #should point to another Node
        
