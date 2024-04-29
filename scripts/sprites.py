import os
import pygame
import numpy as np
from scripts.constantes import *

LARGURA_BLOCO_BASE = 16
ALTURA_BLOCO_BASE = 16

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("assets/Imagens/labirinto.png").convert()
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
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, LARGURA_BLOCO, ALTURA_BLOCO)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        for row in range(self.data.shape[0]):
            for col in range(self.data.shape[1]):
                if self.data[row][col] == '0':
                    # Quinas
                    filepath = os.path.join("assets/Imagens/labirinto", "20_labirinto.png")
                elif self.data[row][col] == '1':
                    # Bordas
                    filepath = os.path.join("assets/Imagens/labirinto", "26_labirinto.png")
                elif self.data[row][col] == '2':
                    # Quinas Dentro
                    filepath = os.path.join("assets/Imagens/labirinto", "26_labirinto.png")
                elif self.data[row][col] == '3':
                    # Bordas Dentro
                    filepath = os.path.join("assets/Imagens/labirinto", "19_labirinto.png")
                elif self.data[row][col] == '4':
                    # Preenchido
                    filepath = os.path.join("assets/Imagens/labirinto", "19_labirinto.png")
                else:
                    continue  
                sprite = pygame.image.load(filepath).convert_alpha()  # Carrega a imagem com transparência
                sprite = pygame.transform.scale(sprite, (LARGURA_BLOCO, ALTURA_BLOCO))  # Redimensiona a imagem
                rotval = int(self.rotdata[row][col])
                sprite = self.rotate(sprite, rotval)
                background.blit(sprite, (col*LARGURA_BLOCO, row*ALTURA_BLOCO))

        return background

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)

class EcomanSprites(object):
    def __init__(self, entidade, image_path):
        self.entidade = entidade
        self.images = {
            "baixo": pygame.image.load(image_path + "submarine_baixo.png").convert_alpha(),
            "cima": pygame.image.load(image_path + "submarine_cima.png").convert_alpha(),
            "esquerda": pygame.image.load(image_path + "submarine_esquerda.png").convert_alpha(),
            "direita": pygame.image.load(image_path + "submarine_direita.png").convert_alpha()
        }

        self.entidade.image = self.images["esquerda"]

    def update(self):
        if self.entidade.vivo:
            if self.entidade.direction == CIMA:
                self.entidade.image = self.images["cima"]
            elif self.entidade.direction == BAIXO:
                self.entidade.image = self.images["baixo"]
            elif self.entidade.direction == ESQUERDA:
                self.entidade.image = self.images["esquerda"]
            elif self.entidade.direction == DIREITA:
                self.entidade.image = self.images["direita"]

class ColetavelSprites(object):
    def __init__(self, coletavel, image_path):
        self.coletavel = coletavel
        self.image = pygame.image.load(image_path).convert_alpha()

    # def setImage(self, image_path):
    #     self.image = pygame.image.load(image_path).convert_alpha()

class InimigoSprites(object):
    def __init__(self, entidade, image_path):
        self.entidade = entidade
        self.images = {
            "baixo": pygame.transform.scale(pygame.image.load(image_path + "tubarao_baixo.png").convert_alpha(), (LARGURA_BLOCO * 2, ALTURA_BLOCO * 2)),
            "cima": pygame.transform.scale(pygame.image.load(image_path + "tubarao_cima.png").convert_alpha(), (LARGURA_BLOCO * 2, ALTURA_BLOCO * 2)),
            "esquerda": pygame.transform.scale(pygame.image.load(image_path + "tubarao_esquerda.png").convert_alpha(), (LARGURA_BLOCO * 2, ALTURA_BLOCO * 2)),
            "direita": pygame.transform.scale(pygame.image.load(image_path + "tubarao_direita.png").convert_alpha(), (LARGURA_BLOCO * 2, ALTURA_BLOCO * 2))
        }
        self.entidade.image = self.images["direita"]

    def update(self):
        if self.entidade.direction == CIMA:
            self.entidade.image = self.images["cima"]
        elif self.entidade.direction == BAIXO:
            self.entidade.image = self.images["baixo"]
        elif self.entidade.direction == ESQUERDA:
            self.entidade.image = self.images["esquerda"]
        elif self.entidade.direction == DIREITA:
            self.entidade.image = self.images["direita"]

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


