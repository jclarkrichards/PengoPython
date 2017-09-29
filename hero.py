import pygame
from constants import *
import math
from math import floor
from vectors import Vector2D
from node import Node

class Hero(object):
    def __init__(self, x, y):
        '''x and y are in array units'''
        self.position = Vector2D(x, y)
        #self.dirVec = Vector2D()
        #self.target = None
        self.resetVariables()
        # Colliders
        self.rightColliders = []
        self.leftColliders = []
        self.topColliders = []
        self.bottomColliders = []
        self.rightCornerCollider = []
        self.leftCornerCollider = []
        self.defineColliders()
        self.direction = "RIGHT" #"LEFT"
        self.speed = 7
        self.reportOvershotData = False
        self.test = False

    def resetVariables(self, midpath=False):
        '''Reset variables to starting conditions'''
        self.setGhostPosition(Vector2D(self.position.x, self.position.y))
        self.node = Node(self.position.x, self.position.y, first=True)
        self.target = self.node
        t = self.target.position - self.node.position
        self.dirVec = t.normalize()
        self.nodeList = [self.node]
        self.foundPath = False
        self.showPath = False
        self.followPath = False
        self.path = [(self.ghost_position.x*WIDTH, self.ghost_position.y*HEIGHT)]
        """
        print "RESETTING VARIABLES"
        print "Ghost"
        print self.ghost_position
        print "Me"
        print self.position
        print "Node"
        print self.node.position
        print "Target"
        print self.target.position
        print "Node list = " + str(len(self.nodeList))
        print "Direction"
        print self.dirVec
        print ""
        """
    def resetVariablesMidPath(self):
        '''This is called when a tetris piece has been placed.  Need to modify path'''
        #self.position = self.node.position.copy()
        self.setGhostPosition(self.node.position.copy())
        #self.ghost_position = self.target.position.copy()
        self.node = Node(self.node.position.x, self.node.position.y, first=True)
        self.test = True
        #self.target = Node(self.target.position.x, self.target.position.y)
        #self.node.nextNode = self.target
        #t = self.target.position - self.node.position
        #self.dirVec = t.normalize()
        #print self.dirVec
        self.nodeList = [self.node]
        self.foundPath = False
        self.showPath = False
        #self.followPath = False
        self.path = [(self.ghost_position.x*WIDTH, self.ghost_position.y*HEIGHT)]
        """
        print "Modify the path"
        print "Ghost"
        print self.ghost_position
        print "Me"
        print self.position
        print "Node"
        print self.node.position
        print "Target"
        print self.target.position
        print "Node list = " + str(len(self.nodeList))
        print "Direction"
        print self.dirVec
        """
        
    def update(self, dt):
        '''Follow the path from one node to the next'''
        self.position += self.dirVec*self.speed*dt
        #print "Pengo Update", self.node.position, self.target.position, self.dirVec
        if self.overshotTarget():
            #self.position = self.target.position
            #print "OVERSHOT"
            if self.target.position != self.target.nextNode.position:
                #print "continue on your way"
                #There is another node to move towards
                #print self.node.position, self.node.nextNode.position, self.target.position
                self.node = self.target
                self.target = self.node.nextNode
                self.position = self.node.position
                t = self.target.position - self.node.position
                self.dirVec = t.normalize()
                #if self.dirVec.magnitudeSquared() == 0:
            else:#Dead end
                #print "DEAD END.  REVERSE"
                #print self.position, self.target.position, self.target.nextNode.position
                self.position = self.target.position
                if self.direction == "RIGHT": 
                    self.direction = "LEFT"
                else:
                    self.direction = "RIGHT"
                #print "Change direction to "+self.direction
                self.resetVariables()
            #else:
            #    self.position = self.node.position

    def overshotTarget(self):
        vec1 = self.target.position - self.node.position
        vec2 = self.position - self.node.position
        node2target = vec1.magnitudeSquared()
        node2self = vec2.magnitudeSquared()
        return node2self >= node2target
    
    def updatePlayArea(self, playfield):
        self.playfield = playfield

    def queryGrid(self, vec):
        '''Return the value at the specified row and column vector'''
        return self.playfield[vec.y, vec.x]

    def getPath(self):
        '''Gotta check the down colliders first'''
        #print len(self.nodeList)
        #Use colliders to check for collisions before moving
        if self.direction == "RIGHT":
            if (self.queryGrid(self.bottomColliders[0]) != 0 or
                self.queryGrid(self.bottomColliders[1]) != 0):
                #print "Cannot move down, check if we can move RIGHT"
                if self.queryGrid(self.rightColliders[0]) != 0:
                    #print "Front upper collision, gotta go LEFT"
                    self.jumpToFirstNode()
                elif self.queryGrid(self.rightColliders[1]) != 0:
                    #print "Front bottom collision, check the three top colliders"
                    if (self.queryGrid(self.topColliders[0]) != 0 or
                        self.queryGrid(self.topColliders[1]) != 0 or
                        self.queryGrid(self.rightCornerCollider) != 0):
                        #print "The top is being blocked, reverse direction"
                        self.jumpToFirstNode()
                    else:
                        #print "Move UP"
                        self.moveGhost(UPRIGHT)
                        self.linkNodes()
                else:
                    #print "No front colliders, proceed RIGHT"
                    self.moveGhost(RIGHT)
                    self.linkNodes()                    
            else:
                #print "Gotta move down man"
                self.moveGhost(DOWN)
                self.linkNodes()

        else:
            if (self.queryGrid(self.bottomColliders[0]) != 0 or
                self.queryGrid(self.bottomColliders[1]) != 0):
                #print "Cannot move down, check if we can move LEFT"
                if self.queryGrid(self.leftColliders[0]) != 0:
                    #print "Front upper collision, gotta go LEFT"
                    self.jumpToFirstNode()

                elif self.queryGrid(self.leftColliders[1]) != 0:
                    #print "Front bottom collision, check the three top colliders"
                    if (self.queryGrid(self.topColliders[0]) != 0 or
                        self.queryGrid(self.topColliders[1]) != 0 or
                        self.queryGrid(self.leftCornerCollider) != 0):
                        #print "The top is being blocked, reverse direction"
                        self.jumpToFirstNode()
                    else:
                        #print "Move UP"
                        self.moveGhost(UPLEFT)
                        self.linkNodes()
                else:
                    #print "No front colliders, proceed RIGHT"
                    self.moveGhost(LEFT)
                    self.linkNodes()
            else:
                #print "Gotta move down man"
                self.moveGhost(DOWN)
                self.linkNodes()
            

    def linkNodes(self):
        '''Link all of the nodes in the path list together'''
        x, y = self.ghost_position.toTuple()
        self.node.nextNode = Node(x, y)
        self.node = self.node.nextNode
        #print "test", self.node.position
        self.nodeList.append(self.node)

    def jumpToFirstNode(self):
        '''Find the first node in the sequence'''
        #print "TIME TO REVERSE DIRECTION"
        #print "PATH FOUND WITH  " + str(len(self.nodeList)) +" NODES"
        #for i in range(len(self.nodeList)):
        #    print self.nodeList[i].position
        #print ""
        self.showPath = True
        self.foundPath = True
        self.followPath = True
        for node in self.nodeList:
            if node.first:
                self.node = node
                #print "Found first node"
                #print self.node.position
                #print self.node.nextNode.position
                #print self.target.position
                #print ""
                #self.target = self.node.nextNode
                break
                
        #This is just for showing the path
        #Go through the nodes and get their positions, then jump back to the first node
        while self.node != self.node.nextNode:
            self.node = self.node.nextNode
            x, y = self.node.position.toTuple()
            self.path.append((x*WIDTH, y*HEIGHT))
        #print "Path List"
        #print self.path
        for node in self.nodeList:
            if node.first:
                self.node = node
                break
        
        self.target = self.node.nextNode
        self.getDirection()
        #if self.test:
        #    self.test = False
        #    print "NEW TARGET"
        #    self.target = self.node.nextNode
        #print "test", self.node.position, self.target.position

    def moveGhost(self, vec):
        '''Add the vec to all of the collider vectors'''
        self.ghost_position += vec
        for i in range(len(self.rightColliders)):
            self.rightColliders[i] += vec
        for i in range(len(self.leftColliders)):
            self.leftColliders[i] += vec
        for i in range(len(self.topColliders)):
            self.topColliders[i] += vec
        for i in range(len(self.bottomColliders)):
            self.bottomColliders[i] += vec
        self.rightCornerCollider += vec
        self.leftCornerCollider += vec

    def setGhostPosition(self, position):
        '''When setting the ghost position need to reset all of its colliders too'''
        self.ghost_position = position
        self.defineColliders()

    def getDirection(self):
        t = self.target.position - self.node.position
        self.dirVec = t.normalize()
        
    def defineColliders(self):
        '''Define the initial position of all of the colliders'''
        x, y = self.ghost_position.toTuple()
        self.rightColliders = [Vector2D(x+2, y), Vector2D(x+2, y+1)]
        self.leftColliders = [Vector2D(x-1, y), Vector2D(x-1, y+1)]
        self.topColliders = [Vector2D(x, y-1), Vector2D(x+1, y-1)]
        self.bottomColliders = [Vector2D(x, y+2), Vector2D(x+1, y+2)]
        self.rightCornerCollider = Vector2D(x+2, y-1)
        self.leftCornerCollider = Vector2D(x-1, y-1)

    def render(self, screen, showColliders=False):
        x, y = self.position.toTuple()
        pygame.draw.rect(screen, YELLOW, [x*WIDTH, y*HEIGHT, 2*WIDTH, 2*HEIGHT])

        if showColliders:
            for rc in self.rightColliders:
                pygame.draw.rect(screen, GRAY, [rc.x*WIDTH, rc.y*HEIGHT, WIDTH, HEIGHT])
            for lc in self.leftColliders:
                pygame.draw.rect(screen, GRAY, [lc.x*WIDTH, lc.y*HEIGHT, WIDTH, HEIGHT])
            for tc in self.topColliders:
                pygame.draw.rect(screen, GRAY, [tc.x*WIDTH, tc.y*HEIGHT, WIDTH, HEIGHT])
            for bc in self.bottomColliders:
                pygame.draw.rect(screen, GRAY, [bc.x*WIDTH, bc.y*HEIGHT, WIDTH, HEIGHT])
            
            pygame.draw.rect(screen, GRAY, [self.rightCornerCollider.x*WIDTH, self.rightCornerCollider.y*HEIGHT, WIDTH, HEIGHT])
            pygame.draw.rect(screen, GRAY, [self.leftCornerCollider.x*WIDTH, self.leftCornerCollider.y*HEIGHT, WIDTH, HEIGHT])

        if self.showPath:
            for i in range(len(self.path)-1):
                pygame.draw.line(screen, WHITE, self.path[i], self.path[i+1]) 
