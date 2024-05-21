import pygame
from scripts.vetor import Vector2
import numpy as np
from scripts.constantes import *
from scripts.sprites import ColetavelSprites

class Coletavel(object):
    def __init__(self, row, column):
        self.nome = COLETAVEL
        self.linha = row  # Armazena a posição da linha
        self.coluna = column  # Armazena a posição da coluna
        self.posicao = Vector2(column*LARGURA_BLOCO, row*ALTURA_BLOCO)
        self.pontuacao = 800
        self.visivel = True  # Define a visibilidade inicial do coletável
        self.raio = int(2 * LARGURA_BLOCO / 16)
        self.raio_colisao = int(2 * ALTURA_BLOCO / 16)
        self.sprites = ColetavelSprites(self, "assets/Imagens/coletavel.png")

    def render(self, screen):
        if self.visivel:
            self.raio = int(2 * LARGURA_BLOCO / 16)
            self.raio_colisao = int(2 * LARGURA_BLOCO / 16)
            sprite_position = (self.posicao.x, self.posicao.y - LARGURA_BLOCO)
            screen.blit(self.sprites.image, sprite_position)
    
class GrupoColetaveis(object):
    def __init__(self, pelletfile):
        self.lista_coletaveis = []
        self.criar_lista_coletaveis(pelletfile)
        self.coletados = 0
                
    def criar_lista_coletaveis(self, pelletfile):
        data = self.ler_arquivo(pelletfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['P', 'p']:
                    self.lista_coletaveis.append(Coletavel(row, col))
                    
    def ler_arquivo(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def esta_vazio(self):
        if len(self.lista_coletaveis) == 0:
            return True
        return False
    
    def render(self, screen):
        for coletavel in self.lista_coletaveis:
            coletavel.render(screen)
