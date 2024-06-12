import pygame
import numpy as np
from scripts.vetor import Vector2
from scripts.constantes import *

class Node(object):
    def __init__(self, x, y):
        self.posicao = Vector2(x, y)
        self.vizinhos = {CIMA:None, BAIXO:None, ESQUERDA:None, DIREITA:None}

    def render(self, screen):
        for n in self.vizinhos.keys():
            if self.vizinhos[n] is not None:
                line_start = self.posicao.forma_tupla()
                line_end = self.vizinhos[n].posicao.asTuple()
                pygame.draw.line(screen, BRANCO, line_start, line_end, 4)
                pygame.draw.circle(screen, VERMELHO, self.posicao.forma_inteiro(), 12)


class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nos = {}
        self.simbolo_nos = ['+', 'n', 'p', 'P']
        self.simbolo_caminhos = ['.', '-', '|', 'p', 'P', 'E', 'I']
        data = self.ler_arquivo_libirinto(level)
        self.criar_nodetable(data)
        self.conectar_horizontal(data)
        self.conectar_vertical(data)

    def ler_arquivo_libirinto(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def criar_nodetable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.simbolo_nos:
                    x, y = self.construir(col+xoffset, row+yoffset)
                    self.nos[(x, y)] = Node(x, y)
    
    def construir(self, x, y):
        return x * LARGURA_BLOCO, y * ALTURA_BLOCO
    
    # Conectar os nós na horizontal
    def conectar_horizontal(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.simbolo_nos:
                    if key is None:
                        key = self.construir(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.construir(col+xoffset, row+yoffset)
                        self.nos[key].vizinhos[DIREITA] = self.nos[otherkey]
                        self.nos[otherkey].vizinhos[ESQUERDA] = self.nos[key]
                        key = otherkey
                elif data[row][col] not in self.simbolo_caminhos:
                    key = None

    # Conectar os nós na vertical
    def conectar_vertical(self, data, xoffset=0, yoffset=0):
        data_transposta = data.transpose()
        for col in list(range(data_transposta.shape[0])):
            key = None
            for row in list(range(data_transposta.shape[1])):
                if data_transposta[col][row] in self.simbolo_nos:
                    if key is None:
                        key = self.construir(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.construir(col+xoffset, row+yoffset)
                        self.nos[key].vizinhos[BAIXO] = self.nos[otherkey]
                        self.nos[otherkey].vizinhos[CIMA] = self.nos[key]
                        key = otherkey
                elif data_transposta[col][row] not in self.simbolo_caminhos:
                    key = None

    # Obter os pixels de um nó
    def obter_no_pixel(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nos.keys():
            return self.nos[(xpixel, ypixel)]
        return None

    # Obter a linha e coluna de um nó
    def obter_no_tiles(self, col, row):
        x, y = self.construir(col, row)
        if (x, y) in self.nos.keys():
            return self.nos[(x, y)]
        return None
    
    # Nó inicial
    def no_inicial(self, valor):
        nodes = list(self.nos.values())
        return nodes[valor] if valor != 0 else nodes[3]

    def render(self, screen):
        for node in self.nos.values():
            node.render(screen)