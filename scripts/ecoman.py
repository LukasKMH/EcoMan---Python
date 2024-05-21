import pygame
from pygame.locals import *
import numpy as np
from scripts.vetor import Vector2
from scripts.constantes import *
from scripts.personagem import Personagem
from scripts.sprites import EcomanSprites

class Ecoman(Personagem):
    def __init__(self, node):
        Personagem.__init__(self, node)
        self.nome = ECOMAN
        self.direcao = PARAR
        self.raio = 10
        self.raio_colisao = self.raio * 0.9
        self.cor = LARANJA
        self.definir_velocidade(250)
        self.vivo = True
        self.sprite = EcomanSprites(self, "assets/Imagens/ecoman/")
        
    def update(self, dt):
        self.posicao += self.direcoes[self.direcao]*self.speed*dt
        direction = self.getValidKey()
        self.sprite.update()
        
        if self.ultrapassou_alvo():
            self.node = self.alvo
            self.alvo = self.novo_alvo(direction)
            if self.alvo is not self.node:
                self.direcao = direction
            else:
                self.alvo = self.novo_alvo(self.direcao)

            if self.alvo is self.node:
                self.direcao = PARAR
            self.definir_posicao()
        else: 
            if self.direcao_oposta(direction):
                self.reverter_direcao()

    # Movimento
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP] or key_pressed[K_w]:
            return CIMA
        if key_pressed[K_DOWN] or key_pressed[K_s]:
            return BAIXO
        if key_pressed[K_LEFT] or key_pressed[K_a]:
            return ESQUERDA
        if key_pressed[K_RIGHT] or key_pressed[K_d]:
            return DIREITA
        return PARAR

    def coletar(self, lista_coletaveis):
        for coletavel in lista_coletaveis:
            if self.collideCheck(coletavel):
                return coletavel
        return None 
    
    def colideInimigo(self, inimigo):
        return self.collideCheck(inimigo)

    def collideCheck(self, other):
        distancia = self.posicao - other.posicao
        dist_quadrado = distancia.magnitude_quadrada()
        raio_quadrado = (self.raio + other.raio)**2
        if dist_quadrado <= raio_quadrado:
            return True
        return False

    def reset(self):
        Personagem.reset(self)
        self.direcao = ESQUERDA
        self.entre_os_nos(ESQUERDA)
        self.alive = True

    def die(self):
        self.alive = False
        self.direcao = PARAR
