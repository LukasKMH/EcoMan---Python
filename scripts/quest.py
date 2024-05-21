import pygame
from scripts.personagem import Personagem
from scripts.constantes import *

class Quest(Personagem):
    def __init__(self, node):
        Personagem.__init__(self, node)
        self.name = QUEST
        self.color = VERDE
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.entre_os_nos(DIREITA)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
    
    

