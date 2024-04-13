import pygame
from pygame.locals import *
from vetor import Vector2
from constantes import *
from personagem import Personagem


class Ecoman(Personagem):
    def __init__(self, node):
        Personagem.__init__(self, node )
        self.name = ECOMAN
        #self.directions = {PARAR:Vector2(), CIMA:Vector2(0,-1), BAIXO:Vector2(0,1), ESQUERDA:Vector2(-1,0), DIREITA:Vector2(1,0)}
        self.direction = PARAR
        #self.speed = 100 * LARGURA_BLOCO/16
        self.radius = 10
        self.collideRadius = self.radius * 0.9
        self.color = LARANJA
        self.setBetweenNodes(ESQUERDA)
        # self.node = node
        # self.setPosition()
        # self.target = node

    # def setPosition(self):
    #     self.position = self.node.position.copy()

    def update(self, dt):	
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        
        if self.overshotTarget():
            self.node = self.target
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = PARAR
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    # Movimento
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP] or key_pressed[K_w]:
            return CIMA
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            return BAIXO
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            return ESQUERDA
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            return DIREITA
        return PARAR

    def eatPellets(self, listaColetaveis):
        for coletavel in listaColetaveis:
            if self.collideCheck(coletavel):
                return coletavel
        return None 
    
    def colideInimigo(self, inimigo):
        return self.collideCheck(inimigo)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.radius + other.radius)**2
        if dSquared <= rSquared:
            return True
        return False
    
