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
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'n', 'p', 'P']
        self.pathSymbols = ['.', '-', '|', 'p', 'P', 'E', 'I']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.conectar_horizontal(data)
        self.conectar_vertical(data)

    def readMazeFile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)
    
    def constructKey(self, x, y):
        return x * LARGURA_BLOCO, y * ALTURA_BLOCO
    
    # Conectar os nós na horizontal
    def conectar_horizontal(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].vizinhos[DIREITA] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].vizinhos[ESQUERDA] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    # Conectar os nós na vertical
    def conectar_vertical(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].vizinhos[BAIXO] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].vizinhos[CIMA] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    # Obter os pixels de um nó
    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    # Obter a linha e coluna de um nó
    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None
    
    # Nó inicial
    def getStartTempNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[3]
    
    def startInimigos(self, valor):
        nodes = list(self.nodesLUT.values())
        return nodes[valor]

    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)