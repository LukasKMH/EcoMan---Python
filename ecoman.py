import pygame
from pygame.locals import *
from vetor import Vector2
from scripts.constantes import *
from personagem import Personagem
import numpy as np
from sprites import EcomanSprites

class Ecoman(Personagem):
    def __init__(self, node):
        Personagem.__init__(self, node)
        self.name = ECOMAN
        self.direction = PARAR
        self.radius = 10
        self.collideRadius = self.radius * 0.9
        self.color = LARANJA
        self.setSpeed(250)
        self.setBetweenNodes(ESQUERDA)
        self.vivo = True
        self.sprite = EcomanSprites(self, "assets/Imagens/submarine.png")

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
    
    def reset(self):
        Personagem.reset(self)
        self.direction = ESQUERDA
        self.setBetweenNodes(ESQUERDA)
        self.alive = True

    def die(self):
        self.alive = False
        self.direction = PARAR
                
    def createEcoman(self, file):
        data = self.lerArquivo(file)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['E',]:
                    Ecoman(row, col)
                    
    def lerArquivo(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
