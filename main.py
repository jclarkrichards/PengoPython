import pygame
from pygame.locals import *
from constants import *
from random import randint
import numpy as np
from bag import Bag
from playarea import PlayField
from hero import Hero

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.background = None
        self.setBackGround()
        self.playfield = PlayField()
        self.bag = Bag(7)
        self.activePiece = self.bag.getNextPiece()
        self.activePiece.A = self.playfield.A
        self.pengo = Hero(1,5)
        self.pengo.updatePlayArea(self.playfield.A)
        self.paused = False
        self.printOnce = True

    def setBackGround(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def update(self):
        dt = self.clock.tick(30)/1000.0
        if not self.paused:
            #print self.pengo.node.position, self.pengo.target.position
            self.activePiece.update(dt)
            # A tetris piece has been placed
            if not self.activePiece.alive:
                self.playfield.addPiece(self.activePiece)
                self.activePiece = self.bag.getNextPiece()
                self.activePiece.A = self.playfield.A
                self.pengo.updatePlayArea(self.playfield.A)
                #print ""
                #print self.pengo.playfield
                #print ""
                self.pengo.resetVariablesMidPath()
                self.pengo.reportOvershotData = True

            while not self.pengo.foundPath:
                self.pengo.getPath()
            if self.printOnce:
                #print "After getPath", self.pengo.node.position, self.pengo.target.position
                self.printOnce = False
            #self.checkEvents(dt)

            if self.pengo.followPath:
                self.pengo.update(dt)
        self.checkEvents(dt)
        self.render()

    def checkEvents(self, dt):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_LEFT]:
            self.activePiece.moveLeftContinuous(dt)
        elif key_pressed[K_RIGHT]:
            self.activePiece.moveRightContinuous(dt)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    self.activePiece.moveLeft()
                elif event.key == K_RIGHT:
                    self.activePiece.moveRight()
                
                if event.key == K_z:
                    self.activePiece.rotateCCW()
                elif event.key == K_x:
                    self.activePiece.rotateCW()
                
                if event.key == K_DOWN:
                    self.activePiece.fallSpeed *= 6
                
                if event.key == K_SPACE:
                    self.paused = not self.paused

            elif event.type == KEYUP:
                if event.key == K_DOWN:
                    self.activePiece.fallSpeed = self.activePiece.normalSpeed
                if event.key == K_LEFT or event.key == K_RIGHT:
                    self.activePiece.left_right_timer = 0



    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.activePiece.render(self.screen)
        self.playfield.render(self.screen)
        self.pengo.render(self.screen, showColliders=False)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    #game.startGame()
    while True:
        game.update()
