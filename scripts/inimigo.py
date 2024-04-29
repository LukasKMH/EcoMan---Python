import pygame
from pygame.locals import *
from scripts.vetor import Vector2
from scripts.constantes import *
from scripts.personagem import Personagem
from scripts.sprites import InimigoSprites

class Inimigo(Personagem):
    def __init__(self, node):
        Personagem.__init__(self, node)
        self.name = INIMIGO
        self.points = 200
        self.collideRadius = self.radius
        self.speed = 150
        self.sprite = InimigoSprites(self, "assets/Imagens/inimigos/")

    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
        self.sprite.update()
        
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

    def reset(self):
        Personagem.reset(self)
        self.directionMethod = self.goalDirection
