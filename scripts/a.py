import pygame
from pygame.locals import *
from random import randint
from scripts.vetor import Vector2
from scripts.constantes import *

class Personagem(object):
    def __init__(self, node):
        self.nome = None
        self.direcoes = {CIMA:Vector2(0, -1),BAIXO:Vector2(0, 1), 
                          ESQUERDA:Vector2(-1, 0), DIREITA:Vector2(1, 0), PARAR:Vector2()}
        self.direcao = PARAR
        self.definir_velocidade(100)
        self.raio = 10
        self.raio_colisao = 5
        self.cor = BRANCO
        self.node = node
        self.definir_posicao()
        self.alvo = node
        self.visivel = True
        self.image = None

    def definir_posicao(self):
        self.posicao = self.node.posicao.copy()
          
    def validar_direcao(self, direction):
        return direction != PARAR and self.node.vizinhos[direction] is not None

    def definir_alvo(self, direction):
        if self.validar_direcao(direction):
            return self.node.vizinhos[direction]
        return self.node

    def ultrapassou_alvo(self):
        if self.alvo is not None:
            vec1 = self.alvo.posicao - self.node.posicao
            vec2 = self.posicao - self.node.posicao
            node2_alvo = vec1.magnitude_quadrada()
            node2_self = vec2.magnitude_quadrada()
            return node2_self >= node2_alvo
        return False

    def reverter_direcao(self):
        self.direcao *= -1
        temp = self.node
        self.node = self.alvo
        self.alvo = temp
        
    def direcao_oposta(self, direction):
        return direction != PARAR and direction == self.direcao * -1

    def definir_velocidade(self, speed):
        self.speed = speed * LARGURA_BLOCO / 16

    def update(self, dt):
        self.posicao += self.direcoes[self.direcao]*self.speed*dt
         
        if self.ultrapassou_alvo():
            self.node = self.alvo
            directions = self.validar_direcao()
            direction = self.direcao_aleatoria(directions)   
            self.alvo = self.definir_alvo(direction)
            if self.alvo is not self.node:
                self.direcao = direction
            else:
                self.alvo = self.definir_alvo(self.direcao)

            self.definir_posicao()

    def validar_direcao(self):
        direcoes = [
            key for key in [CIMA, BAIXO, ESQUERDA, DIREITA]
            if self.validar_direcao(key) and key != self.direcao * -1
        ]
        if not direcoes:
            direcoes.append(self.direcao * -1)
        return direcoes

    def direcao_aleatoria(self, direcoes):
        return direcoes[randint(0, len(direcoes)-1)]
    
    def entre_os_nos(self, direcao):
        if self.node.vizinhos[direcao] is not None:
            self.alvo = self.node.vizinhos[direcao]
            self.posicao = (self.node.posicao + self.alvo.posicao) / 2.0

    def reset(self):
        self.setStartNode(self.startNode)
        self.direcao = PARAR
        self.speed = 100
        self.visivel = True

    def render(self, screen):
        if self.visivel:
            if self.image is not None:
                adjust = Vector2(LARGURA_BLOCO, ALTURA_BLOCO) / 2
                p = self.posicao - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.posicao.asInt()
                pygame.draw.circle(screen, self.cor, p, self.raio)
            
