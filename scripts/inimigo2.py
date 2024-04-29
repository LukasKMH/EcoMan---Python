import pygame
from pygame.locals import *
import numpy as np
from scripts.vetor import Vector2
from scripts.constantes import *
from scripts.personagem import Personagem

class Inimigo(Personagem):
    def __init__(self, row, column):
        self.name = INIMIGO
        self.points = 0  # Pontos associados ao inimigo

    def reset(self):
        super().reset()
        # Adicione aqui qualquer reinicialização específica do inimigo

    def render(self, screen):
        # Desenha o inimigo na tela como um círculo vermelho
        pygame.draw.circle(screen, VERMELHO, (int(self.position.x), int(self.position.y)), self.radius)

class GrupoInimigos(object):
    def __init__(self, inimigosfile):
        self.listaInimigos = []
        self.createInimigosList(inimigosfile)

    def update(self, dt):
        for inimigo in self.listaInimigos:
            inimigo.update(dt)
                
    def createInimigosList(self, inimigosfile):
        data = self.readInimigosfile(inimigosfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['I']:
                    self.listaInimigos.append(Inimigo(row, col))
                    
    def readInimigosfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def isEmpty(self):
        return len(self.listaInimigos) == 0
    
    def render(self, screen):
        for inimigo in self.listaInimigos:
            inimigo.render(screen)
