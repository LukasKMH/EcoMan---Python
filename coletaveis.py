import pygame
from vetor import Vector2
from constantes import *
import numpy as np

class Coletavel(object):
    def __init__(self, row, column):
        self.name = COLETAVEL
        self.row = row  # Armazena a posição da linha
        self.column = column  # Armazena a posição da coluna
        self.position = Vector2(column*LARGURA_BLOCO, row*ALTURA_BLOCO)
        self.radius = int(10 * LARGURA_BLOCO / 16)
        self.points = 800
        # self.flashTime = 0.2
        # self.timer= 0
        self.visible = True  # Define a visibilidade inicial do coletável

    # Pode ser usado para deixar os coletaveis piscando juntamente com as varaiveis flashTime e self.timer
    def update(self, dt):
        pass
    #     self.timer += dt
    #     if self.timer >= self.flashTime:
    #         self.visible = not self.visible  # Inverte a visibilidade
    #         self.timer = 0

    def render(self, screen):
        if self.visible:  # Verifica se o coletável é visível
            # Desenha o coletável na tela como um círculo
            pygame.draw.circle(screen, AMARELO, (self.column * LARGURA_BLOCO, self.row * ALTURA_BLOCO), self.radius)

class GrupoColetaveis(object):
    def __init__(self, pelletfile):
        self.listaColetaveis = []
        self.createPelletList(pelletfile)
        self.numEaten = 0

    def update(self, dt):
        for coletavel in self.listaColetaveis:
            coletavel.update(dt)
                
    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['P', 'p']:
                    self.listaColetaveis.append(Coletavel(row, col))
                    
    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def isEmpty(self):
        if len(self.listaColetaveis) == 0:
            return True
        return False
    
    def render(self, screen):
        for coletavel in self.listaColetaveis:
            coletavel.render(screen)
