import pygame
from scripts.vetor import Vector2
from scripts.constantes import *

class Text(object):
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("PressStart2P-Regular.ttf")
        self.createLabel()

    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)

    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    def setText(self, newtext):
        self.text = str(newtext)
        self.createLabel()

    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    def render(self, screen):
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))

class TextGroup(object):
    def __init__(self):
        self.nextid = 10
        self.alltext = {}
        self.setupText()

    def addText(self, text, color, x, y, size, time=None, id=None):
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    def removeText(self, id):
        self.alltext.pop(id)
        
    def setupText(self):
        size = ALTURA_BLOCO
        self.alltext[LIXO_RESTANTETXT] = Text(str(1).zfill(2), BRANCO, 6*LARGURA_BLOCO, 2*ALTURA_BLOCO, size)
        self.alltext[TEMPOTXT] = Text("1:50", BRANCO, 24*LARGURA_BLOCO, 2*ALTURA_BLOCO, size)
        self.alltext[PONTUACAOTXT] = Text("0".zfill(4), BRANCO, 41*LARGURA_BLOCO, 2*ALTURA_BLOCO, size)
        self.alltext[PAUSETXT] = Text("JOGO PAUSADO", AMARELO, LARGURA_TELA // 2 - LARGURA_BLOCO * 6, ALTURA_TELA / 2, size, visible=False)
        self.addText("LIXO:", BRANCO, 1*LARGURA_BLOCO, 2*ALTURA_BLOCO, size)
        self.addText("TEMPO:", BRANCO, 18*LARGURA_BLOCO, 2*ALTURA_BLOCO, size)
        self.addText("PONTOS:", BRANCO, 34*LARGURA_BLOCO, 2*ALTURA_BLOCO, size)

    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)

    def showText(self, id):
        self.hideText()
        self.alltext[id].visible = True

    def hideText(self):
        self.alltext[PAUSETXT].visible = False

    def atualizarLixoRestante(self, quantidade_restante):
        self.updateText(LIXO_RESTANTETXT, str(quantidade_restante + 1).zfill(2))

    def atualizarTempo(self, segundos):
        if segundos != 0:
            if TEMPOTXT in self.alltext:
                self.updateText(TEMPOTXT, self.formatarTempo(segundos))
                return True
            else:
                return False

    def formatarTempo(self, segundos):
        minutos = segundos // 60
        segundos %= 60
        return "{:02}:{:02}".format(int(minutos), int(segundos))

    def atualizarPontuacao(self, score):
        self.updateText(PONTUACAOTXT, str(score).zfill(4))

    def updateText(self, id, value):
        if id in self.alltext.keys():
            self.alltext[id].setText(value)

    def render(self, screen):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)