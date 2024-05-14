import pygame
from scripts.vetor import Vector2
import numpy as np
from scripts.constantes import *
from scripts.sprites import ColetavelSprites

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

    def update(self, dt):
        pass

    def render(self, screen):
        if self.visible:  # Verifica se o coletável é visível
            # Desenha o sprite do coletável na tela
            self.radius = int(2 * LARGURA_BLOCO / 16)
            self.collideRadius = int(2 * LARGURA_BLOCO / 16)
            position = (int(self.position.x), int(self.position.y))
            #screen.blit(self.sprites.image, position)
            sprite_position = (self.position.x, self.position.y - LARGURA_BLOCO)
            screen.blit(self.sprites.image, sprite_position)
    
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
