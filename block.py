import pygame
from constants import *
from vectors import Vector2D

class Block(object):
    def __init__(self, x, y, color):
        '''x and y are in coordinate units.  color is a tuple'''
        self.position = Vector2D(x, y)
        self.color = color

    def render(self, screen):
        x, y = self.position.toTuple()
        pygame.draw.rect(screen, self.color, [(x+COLUMNOFFSET)*WIDTH, y*HEIGHT, WIDTH, HEIGHT])


class Shape(object):
    def __init__(self, x, y):
        '''x and y are in coordinate units.  Defines center block. color is a tuple'''
        self.name = ""
        self.value = 0
        self.blocks = []
        self.x, self.y = x, y #Center of shape
        self.horizontalSpeed = 8
        self.fallSpeed = 1 #how many units piece traverses in 1 second
        self.normalSpeed = 1
        self.timeAccumulator = 0
        self.left_right_timer = 0
        self.alive = True
        self.A = None #will contain a 20x10 array indicating locations of played pieces

    def update(self, dt):
        self.timeAccumulator += dt
        #print self.fallSpeed
        if self.timeAccumulator >= 1.0/self.fallSpeed:
            self.timeAccumulator = 0
            if self.alive:
                self.moveDown()

    def moveDown(self):
        if not self.onEdgeBottom():
            self.y += 1
            for b in self.blocks:
                b.position.y += 1
        else:
            #print "bottom"
            self.alive = False

        if self.overlapped():
            self.y -= 1
            for b in self.blocks:
                b.position.y -= 1
            #print "Overlapped"
            self.alive = False

    def moveLeftContinuous(self, dt):
        self.left_right_timer += dt
        if self.left_right_timer >= 1.0/self.horizontalSpeed:
            self.left_right_timer = 0
            self.moveLeft()

    def moveRightContinuous(self, dt):
        self.left_right_timer += dt
        if self.left_right_timer >= 1.0/self.horizontalSpeed:
            self.left_right_timer = 0
            self.moveRight()


    def moveLeft(self):
        if not self.onEdgeLeft():
            self.x -= 1
            for b in self.blocks:
                b.position.x -= 1

        if self.overlapped():
            self.x += 1
            for b in self.blocks:
                b.position.x += 1

    def moveRight(self):
        if not self.onEdgeRight():
            self.x += 1
            for b in self.blocks:
                b.position.x += 1

        if self.overlapped():
            self.x -= 1
            for b in self.blocks:
                b.position.x -= 1

    def rotateCW(self):
        '''should also not rotate into other pieces'''
        if self.name != "O":
            for b in self.blocks:
                x, y = b.position.toTuple()
                b.position = Vector2D(self.y+self.x-y, self.y-self.x+x)

            val1 = self.outOfBoundsValueLeft()
            val2 = self.outOfBoundsValueRight()
            val = val1 + val2
            self.x -= val
            for b in self.blocks:
                b.position.x -= val

            if self.overlapped():#Rotate back if overlapped
                for b in self.blocks:
                    x, y = b.position.toTuple()
                    b.position = Vector2D(self.x-self.y+y, self.x+self.y-x)
                

    def rotateCCW(self):
        '''should also not rotate into other pieces'''
        if self.name != "O":
            for b in self.blocks:
                x, y = b.position.toTuple()
                b.position = Vector2D(self.x-self.y+y, self.x+self.y-x)

            val1 = self.outOfBoundsValueLeft()
            val2 = self.outOfBoundsValueRight()
            val = val1 + val2
            self.x -= val
            for b in self.blocks:
                b.position.x -= val

            if self.overlapped(): #rotate back if overlapped
                for b in self.blocks:
                    x, y = b.position.toTuple()
                    b.position = Vector2D(self.y+self.x-y, self.y-self.x+x)


    def outOfBoundsValueLeft(self):
        '''Find block most out of bounds and return that x value'''
        val = 0
        for b in self.blocks:
            if b.position.x < val:
                val = b.position.x
        return val

    def outOfBoundsValueRight(self):
        '''Find block most out of bounds and return that x value'''
        val = 0
        for b in self.blocks:
            if b.position.x > NCOLS-1:
                val = b.position.x - NCOLS + 1
        return val

    def onEdgeLeft(self):
        '''Check if any of the blocks are out of bounds.  Return True if any are'''
        for b in self.blocks:
            if b.position.x == 0:
                return True
        return False

    def onEdgeRight(self):
        '''Check if any of the blocks are out of bounds.  Return True if any are'''
        for b in self.blocks:
            if b.position.x == NCOLS-1:
                return True
        return False

    def onEdgeBottom(self):
        for b in self.blocks:
            if b.position.y == NROWS-1:
                return True
        return False

    def overlapped(self):
        '''Check if any blocks have overlapped with a value in A array'''
        for b in self.blocks:
            if b.position.y >=0 and b.position.x >= 0:
                try:
                    self.A[b.position.y, b.position.x]
                except IndexError:
                    print "Index error"
                    return True
                else:
                    if self.A[b.position.y, b.position.x] != 0:
                        return True
        return False
        

    def T(self):
        self.name = "T"
        self.value = 1
        self.color = PURPLE
        self.blocks.append(Block(self.x, self.y, self.color))
        self.blocks.append(Block(self.x-1, self.y, self.color))
        self.blocks.append(Block(self.x+1, self.y, self.color))
        self.blocks.append(Block(self.x, self.y-1, self.color))

    def S(self):
        self.name = "S"
        self.value = 2
        self.color = GREEN
        self.blocks.append(Block(self.x, self.y, self.color))
        self.blocks.append(Block(self.x+1, self.y, self.color))
        self.blocks.append(Block(self.x, self.y+1, self.color))
        self.blocks.append(Block(self.x-1, self.y+1, self.color))

    def Z(self):
        self.name = "Z"
        self.value = 3
        self.color = RED
        self.blocks.append(Block(self.x, self.y, self.color))
        self.blocks.append(Block(self.x-1, self.y, self.color))
        self.blocks.append(Block(self.x, self.y+1, self.color))
        self.blocks.append(Block(self.x+1, self.y+1, self.color))

    def L(self):
        self.name = "L"
        self.value = 4
        self.color = ORANGE
        self.blocks.append(Block(self.x, self.y, self.color))
        self.blocks.append(Block(self.x, self.y-1, self.color))
        self.blocks.append(Block(self.x, self.y+1, self.color))
        self.blocks.append(Block(self.x+1, self.y+1, self.color))

    def J(self):
        self.name = "J"
        self.value = 5
        self.color = BLUE
        self.blocks.append(Block(self.x, self.y, self.color))
        self.blocks.append(Block(self.x, self.y-1, self.color))
        self.blocks.append(Block(self.x, self.y+1, self.color))
        self.blocks.append(Block(self.x-1, self.y+1, self.color))

    def O(self):
        self.name = "O"
        self.value = 6
        self.color = YELLOW
        self.blocks.append(Block(self.x, self.y, self.color))
        self.blocks.append(Block(self.x+1, self.y, self.color))
        self.blocks.append(Block(self.x+1, self.y+1, self.color))
        self.blocks.append(Block(self.x, self.y+1, self.color))

    def I(self):
        self.name = "I"
        self.value = 7
        self.color = TEAL
        self.blocks.append(Block(self.x, self.y, self.color))
        self.blocks.append(Block(self.x, self.y-1, self.color))
        self.blocks.append(Block(self.x, self.y-2, self.color))
        self.blocks.append(Block(self.x, self.y+1, self.color))

    def render(self, screen):
        for b in self.blocks:
            b.render(screen)
