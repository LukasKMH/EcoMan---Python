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
        if direction is not PARAR:
            if self.node.vizinhos[direction] is not None:
                return True
        return False

    def novo_alvo(self, direction):
        if self.validar_direcao(direction):
            return self.node.vizinhos[direction]
        return self.node

    def ultrapassou_alvo(self):
        if self.alvo is not None:
            vec1 = self.alvo.posicao - self.node.posicao
            vec2 = self.posicao - self.node.posicao
            node2Target = vec1.magnitude_quadrada()
            node2Self = vec2.magnitude_quadrada()
            return node2Self >= node2Target
        return False

    def reverter_direcao(self):
        self.direcao *= -1
        temp = self.node
        self.node = self.alvo
        self.alvo = temp
        
    def direcao_oposta(self, direction):
        if direction is not PARAR:
            if direction == self.direcao * -1:
                return True
        return False

    def definir_velocidade(self, speed):
        self.speed = speed * LARGURA_BLOCO / 16

    def update(self, dt):
        self.posicao += self.direcoes[self.direcao]*self.speed*dt
         
        if self.ultrapassou_alvo():
            self.node = self.alvo
            directions = self.validar_direcoes()
            direction = self.direcao_aleatoria(directions)   
            self.alvo = self.getNewTarget(direction)
            if self.alvo is not self.node:
                self.direcao = direction
            else:
                self.alvo = self.getNewTarget(self.direcao)

            self.definir_posicao()

    def validar_direcoes(self):
        directions = []
        for key in [CIMA, BAIXO, ESQUERDA, DIREITA]:
            if self.validar_direcao(key):
                if key != self.direcao * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direcao * -1)
        return directions

    def direcao_aleatoria(self, directions):
        return directions[randint(0, len(directions)-1)]
    
    def entre_os_nos(self, direction):
        if self.node.vizinhos[direction] is not None:
            self.alvo = self.node.vizinhos[direction]
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
                screen.blit(self.image, p.forma_tupla())
            else:
                p = self.posicao.forma_inteiro()
                pygame.draw.circle(screen, self.cor, p, self.raio)
            
