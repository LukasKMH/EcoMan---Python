import pygame
from vetor import Vector2
from scripts.constantes import *
import numpy as np
from sprites import ColetavelSprites

class Coletavel(object):
    def __init__(self, row, column):
        self.name = COLETAVEL
        self.row = row  # Armazena a posição da linha
        self.column = column  # Armazena a posição da coluna
        self.position = Vector2(column*LARGURA_BLOCO, row*ALTURA_BLOCO)
        self.radius = int(10 * LARGURA_BLOCO / 16)
        self.points = 800
        self.visible = True  # Define a visibilidade inicial do coletável
        self.radius = int(2 * LARGURA_BLOCO / 16)
        self.collideRadius = int(2 * ALTURA_BLOCO / 16)
        self.sprites = ColetavelSprites(self, "assets/Imagens/coletavel.png")
        # self.flashTime = 0.2
        # self.timer= 0

    # Pode ser usado para deixar os coletaveis piscando juntamente com as varaiveis flashTime e self.timer
    def update(self, dt):
        pass
    #     self.timer += dt
    #     if self.timer >= self.flashTime:
    #         self.visible = not self.visible  # Inverte a visibilidade
    #         self.timer = 0

    def render(self, screen):
        if self.visible:  # Verifica se o coletável é visível
            # Desenha o sprite do coletável na tela
            self.radius = int(2 * LARGURA_BLOCO / 16)
            self.collideRadius = int(2 * LARGURA_BLOCO / 16)
            position = (int(self.position.x), int(self.position.y))
            screen.blit(self.sprites.image, position)



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
