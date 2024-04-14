import pygame
from vetor import Vector2
from constantes import *
import numpy as np

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {CIMA:None, BAIXO:None, ESQUERDA:None, DIREITA:None}

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, BRANCO, line_start, line_end, 4)
                pygame.draw.circle(screen, VERMELHO, self.position.asInt(), 12)


class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'n']
        self.pathSymbols = ['.', '-', '|', 'p', 'P', 'E', 'I']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

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
    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[DIREITA] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[ESQUERDA] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    # Conectar os nós na vertical
    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[BAIXO] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[CIMA] = self.nodesLUT[key]
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
        return nodes[0]

    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)