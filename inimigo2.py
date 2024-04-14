import pygame
from pygame.locals import *
from vetor import Vector2
from constantes import *
from personagem import Personagem
import numpy as np

class Inimigo2(Personagem):
    def __init__(self, row, column):
        self.name = INIMIGO
        self.row = row  # Armazena a posição da linha
        self.column = column  # Armazena a posição da coluna
        self.position = Vector2(column*LARGURA_BLOCO, row*ALTURA_BLOCO)
        self.radius = int(10 * LARGURA_BLOCO / 16)
        self.points = 800
        self.visible = True  # Define a visibilidade inicial do coletável

    def reset(self):
        Personagem.reset(self)
        self.directionMethod = self.goalDirection

    def render(self, screen):
        if self.visible:  # Verifica se o coletável é visível
            # Desenha o coletável na tela como um círculo
            pygame.draw.circle(screen, AMARELO, (self.column * LARGURA_BLOCO, self.row * ALTURA_BLOCO), self.radius)

class GrupoInimigos(object):
    def __init__(self, pelletfile):
        self.listaInimigos = []
        self.createPelletList(pelletfile)

    def update(self, dt):
        for coletavel in self.listaInimigos:
            coletavel.update(dt)
                
    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['I']:
                    self.listaInimigos.append(Inimigo2(row, col))
                    
    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def isEmpty(self):
        if len(self.listaInimigos) == 0:
            return True
        return False
    
    def render(self, screen):
        for coletavel in self.listaInimigos:
            coletavel.render(screen)
