import pygame
from pygame.locals import *
from vetor import Vector2
from constantes import *

class Ecoman(object):
    def __init__(self, node):
        self.name = ECOMAN
        self.directions = {PARAR:Vector2(), CIMA:Vector2(0,-1), BAIXO:Vector2(0,1), ESQUERDA:Vector2(-1,0), DIREITA:Vector2(1,0)}
        self.direction = PARAR
        self.speed = 100 * LARGURA_BLOCO/16
        self.radius = 10
        self.collideRadius = self.radius * 0.9
        self.color = LARANJA
        self.node = node
        self.setPosition()
        self.target = node

    def setPosition(self):
        self.position = self.node.position.copy()

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
        
    def validDirection(self, direction):
        if direction is not PARAR:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

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
            d = self.position - coletavel.position
            dSquared = d.magnitudeSquared()
            rSquared = (coletavel.radius+self.collideRadius)**2
            if dSquared <= rSquared:
                return coletavel
        return None 
    
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False
    
    # Inverter a direção
    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    # Verificar se a direçõe é oposta
    def oppositeDirection(self, direction):
        if direction is not PARAR:
            if direction == self.direction * -1:
                return True
        return False
    
    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)