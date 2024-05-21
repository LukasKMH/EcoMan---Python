import pygame
from scripts.vetor import Vector2
from scripts.constantes import *

class Text(object):
    def __init__(self, texto, cor, x, y, tamanho, time=None, id=None, visivel=True):
        self.id = id
        self.texto = texto
        self.cor = cor
        self.tamanho = tamanho
        self.visivel = visivel
        self.posicao = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.definir_fonte("PressStart2P-Regular.ttf")
        self.criar_label()

    def definir_fonte(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.tamanho)

    def criar_label(self):
        self.label = self.font.render(self.texto, 1, self.cor)

    def definir_texto(self, newtext):
        self.texto = str(newtext)
        self.criar_label()

    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    def render(self, screen):
        if self.visivel:
            x, y = self.posicao.forma_tupla()
            screen.blit(self.label, (x, y))

class GrupoTexto(object):
    def __init__(self):
        self.proximo_id = 10
        self.textos = {}
        self.configurar_texto()

    def adicionar_texto(self, text, cor, x, y, tamanho, time=None, id=None):
        self.proximo_id += 1
        self.textos[self.proximo_id] = Text(text, cor, x, y, tamanho, time=time, id=id)
        return self.proximo_id

    def remover_texto(self, id):
        self.textos.pop(id)
        
    def configurar_texto(self):
        tamanho = ALTURA_BLOCO
        self.textos[LIXO_RESTANTETXT] = Text(str(1).zfill(2), BRANCO, 6*LARGURA_BLOCO, 2*ALTURA_BLOCO, tamanho)
        self.textos[TEMPOTXT] = Text("1:50", BRANCO, 24*LARGURA_BLOCO, 2*ALTURA_BLOCO, tamanho)
        self.textos[PONTUACAOTXT] = Text("0".zfill(4), BRANCO, 41*LARGURA_BLOCO, 2*ALTURA_BLOCO, tamanho)
        self.textos[PAUSETXT] = Text("JOGO PAUSADO", AMARELO, LARGURA_TELA // 2 - LARGURA_BLOCO * 6, ALTURA_TELA / 2, tamanho, visivel=False)
        self.adicionar_texto("LIXO:", BRANCO, 1*LARGURA_BLOCO, 2*ALTURA_BLOCO, tamanho)
        self.adicionar_texto("TEMPO:", BRANCO, 18*LARGURA_BLOCO, 2*ALTURA_BLOCO, tamanho)
        self.adicionar_texto("PONTOS:", BRANCO, 34*LARGURA_BLOCO, 2*ALTURA_BLOCO, tamanho)

    def update(self, dt):
        for texto in list(self.textos.keys()):
            self.textos[texto].update(dt)
            if self.textos[texto].destroy:
                self.remover_texto(texto)

    def mostrar_texto(self, id):
        self.esconder_texto()
        self.textos[id].visivel = True

    def esconder_texto(self):
        self.textos[PAUSETXT].visivel = False

    def atualizar_lixo(self, quantidade_restante):
        self.atualizar_texto(LIXO_RESTANTETXT, str(quantidade_restante + 1).zfill(2))

    def atualizar_tempo(self, segundos):
        if segundos != 0:
            if TEMPOTXT in self.textos:
                self.atualizar_texto(TEMPOTXT, self.formatar_tempo(segundos))
                return True
            else:
                return False

    def formatar_tempo(self, segundos):
        minutos = segundos // 60
        segundos %= 60
        return "{:02}:{:02}".format(int(minutos), int(segundos))

    def atualizar_pontuacao(self, score):
        self.atualizar_texto(PONTUACAOTXT, str(score).zfill(4))

    def atualizar_texto(self, id, value):
        if id in self.textos.keys():
            self.textos[id].definir_texto(value)

    def render(self, screen):
        for texto in list(self.textos.keys()):
            self.textos[texto].render(screen)