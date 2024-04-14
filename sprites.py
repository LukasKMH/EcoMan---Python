import pygame
from constantes import *
import numpy as np

LARGURA_BLOCO_BASE = 16
ALTURA_BLOCO_BASE = 16

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("assets/Imagens/spritesheet.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / LARGURA_BLOCO_BASE * LARGURA_BLOCO)
        height = int(self.sheet.get_height() / ALTURA_BLOCO_BASE * ALTURA_BLOCO)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        
    def getImage(self, x, y, width, height):
        x *= LARGURA_BLOCO
        y *= ALTURA_BLOCO
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

class LabirintoSprites(Spritesheet):
    def __init__(self, mazefile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, LARGURA_BLOCO, ALTURA_BLOCO)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    background.blit(sprite, (col*LARGURA_BLOCO, row*ALTURA_BLOCO))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col*LARGURA_BLOCO, row*ALTURA_BLOCO))

        return background
    
class EcomanSprites(object):
    def __init__(self, entity, image_path):
        self.entity = entity
        self.entity.image = pygame.image.load(image_path).convert_alpha()

    def setImage(self, image_path):
        self.entity.image = pygame.image.load(image_path).convert_alpha()


class NumeroVidas(object):
    def __init__(self, numlives, image_path):
        self.images = []
        self.image_path = image_path
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.loadImage())

    def loadImage(self):
        return pygame.image.load(self.image_path).convert_alpha()

    def setImage(self, image_path):
        self.image_path = image_path
        self.images = [self.loadImage() for _ in range(len(self.images))]


