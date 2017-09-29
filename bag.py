from block import Shape
from random import randint
from constants import *

class Bag(object):
    def __init__(self, num):
        self.numberOfContents = num
        self.contents = []
        self.fillBag()
        #print self.contents

    def fillBag(self):
        '''Fill the bag with random numbers between 0 and numberOfContents'''
        values = range(self.numberOfContents)
        self.contents = []
        while len(values) > 0:
            index = randint(0, len(values)-1)
            self.contents.append(values[index])
            values.remove(values[index])

    def getNextPiece(self):
        '''Return next piece in the bag, if bag is empty then generate a new bag'''
        if len(self.contents) == 0:
            self.fillBag()
        piece = Shape(NCOLS/2, 0)
        value = self.contents.pop()
        if value == 0:
            piece.S()
        elif value == 1:
            piece.Z()
        elif value == 2:
            piece.L()
        elif value == 3:
            piece.J()
        elif value == 4:
            piece.O()
        elif value == 5:
            piece.I()
        elif value == 6:
            piece.T()
        
        return piece
