import pygame
from pygame.locals import *
from random import randint
from scripts.vetor import Vector2
from scripts.constantes import *

class Personagem(object):
    def __init__(self, node):
        self.name = None
        self.directions = {CIMA:Vector2(0, -1),BAIXO:Vector2(0, 1), 
                          ESQUERDA:Vector2(-1, 0), DIREITA:Vector2(1, 0), PARAR:Vector2()}
        self.direction = PARAR
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = BRANCO
        self.node = node
        self.setPosition()
        self.target = node
        self.visible = True
        self.image = None

    def setPosition(self):
        self.position = self.node.position.copy()
          
    def validDirection(self, direction):
        if direction is not PARAR:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp
        
    def oppositeDirection(self, direction):
        if direction is not PARAR:
            if direction == self.direction * -1:
                return True
        return False

    def setSpeed(self, speed):
        self.speed = speed * LARGURA_BLOCO / 16

    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshotTarget():
            self.node = self.target
            directions = self.validDirections()
            direction = self.randomDirection(directions)   
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition()

    def validDirections(self):
        directions = []
        for key in [CIMA, BAIXO, ESQUERDA, DIREITA]:
            if self.validDirection(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)]
    
    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = PARAR
        self.speed = 100
        self.visible = True

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vector2(LARGURA_BLOCO, ALTURA_BLOCO) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)
            
