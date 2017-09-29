import pygame
from constants import *
import numpy as np
from block import Block

class PlayField(object):
    def __init__(self):
        self.A = A #np.zeros((NROWS, NCOLS))
        self.blocks = []
        self.createInitialPieces()

    def createInitialPieces(self):
        for row in range(A.shape[0]):
            for col in range(A.shape[1]):
                if A[row, col] != 0:
                    self.blocks.append(Block(col, row, WHITE))

    def addPiece(self, piece):
        for b in piece.blocks:
            self.A[b.position.y, b.position.x] = piece.value
            self.blocks.append(Block(b.position.x, b.position.y, piece.color))
        #print ""
        #print self.A

    def render(self, screen):
        for b in self.blocks:
            b.render(screen)
                    
