import pygame
from pygame.locals import *
from scripts.vetor import Vector2
from scripts.constantes import *
from scripts.personagem import Personagem
from scripts.sprites import InimigoSprites

class Inimigo(Personagem):
    def __init__(self, node):
        Personagem.__init__(self, node)
        self.nome = INIMIGO
        self.pontuacao = 200
        self.collideRadius = self.raio
        self.velocidade = 150
        self.sprite = InimigoSprites(self, "assets/Imagens/inimigos/")

    def update(self, dt):
        self.posicao += self.direcoes[self.direcao]*self.velocidade*dt
        self.sprite.update()
        
        if self.ultrapassou_alvo():
            self.node = self.alvo
            directions = self.validar_direcoes()
            direction = self.direcao_aleatoria(directions)   
            self.alvo = self.novo_alvo(direction)
            if self.alvo is not self.node:
                self.direcao = direction
            else:
                self.alvo = self.novo_alvo(self.direcao)

            self.definir_posicao()

    def reset(self):
        Personagem.reset(self)
        self.directionMethod = self.goalDirection
