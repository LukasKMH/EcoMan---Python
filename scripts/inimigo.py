import pygame
from pygame.locals import *
from scripts.vetor import Vector2
from scripts.constantes import *
from scripts.personagem import Personagem

class Inimigo(Personagem):
    def __init__(self, node):
        Personagem.__init__(self, node)
        self.name = INIMIGO
        self.points = 200

    def reset(self):
        Personagem.reset(self)
        self.directionMethod = self.goalDirection
