import pygame
import threading
from pygame.locals import *
from scripts.constantes import *
from scripts.ecoman import Ecoman
from scripts.nodes import NodeGroup
from scripts.coletaveis import GrupoColetaveis
from scripts.inimigo import Inimigo
from scripts.quest import Quest
from scripts.pause import Pause
from scripts.texto import TextGroup
from scripts.sprites import NumeroVidas, LabirintoSprites
from scripts.tela_fim_fase import TelaFinal
from scripts.tela_pergunta import QuizApp

class Labirinto(object):
    def __init__(self, mapa, mapa_rotacao, level, vidas, segundos, numero_inimigos):
        pygame.init()
        
        self.vidas2 = vidas
        self.segundos2 = segundos
        
        self.mapa = mapa
        self.mapa_rotacao = mapa_rotacao
        self.screen = pygame.display.set_mode(TAMANHO_TELA, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.pause = Pause(False)
        self.level = level
        self.vidas = vidas
        self.score = 0
        self.segundos = segundos
        self.segundos_aux = 0
        self.textgroup = TextGroup()
        self.nodes = NodeGroup(self.mapa)
        self.lista_inimigos = []
        self.gerarInimigos(numero_inimigos)
        self.lifesprites = NumeroVidas(self.vidas, "assets/Imagens/vida.png")


    def setBackground(self):
        self.background = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.background.fill(AZUL)

    def startGame(self):
        self.setBackground()
        self.quest = Quest(self.nodes.getStartTempNode())
        self.mazesprites = LabirintoSprites(self.mapa, self.mapa_rotacao)
        self.background = self.mazesprites.constructBackground(self.background, self.level%5)
        self.ecoman = Ecoman(self.nodes.getStartTempNode())
        self.coletaveis = GrupoColetaveis(self.mapa)
        self.textgroup.atualizarPontuacao(self.score)
        self.textgroup.atualizarLixoRestante(len(self.coletaveis.listaColetaveis) - 1)
        self.lifesprites.resetLives(self.vidas)
        self.atualizarTempo()
        while True:
            self.update()

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.segundos_aux += 1
        self.textgroup.update(dt)
        self.coletaveis.update(dt)
        if not self.pause.paused:
            self.ecoman.update(dt)
            for inimigo in self.lista_inimigos:
                inimigo.update(dt)
            if self.quest is not None:
                self.quest.update(dt)
            self.checkColetaveisEvento()
            if self.ecoman.collideRadius != 0:
                self.checkInimigoEvento()
            self.checkQuestEvento()
            self.textgroup.atualizarLixoRestante(len(self.coletaveis.listaColetaveis) - 1)
            if self.segundos_aux >= 60:
                self.segundos_aux = 0
                self.segundos -= 1
                self.atualizarTempo()

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def atualizarTempo(self):
        if not self.textgroup.atualizarTempo(self.segundos):
            resultado = TelaFinal("derrota", self).executar()
        
    def gerarInimigos(self, quantidade):
        for _ in range(quantidade):
            i = 22
            novo_inimigo = Inimigo(self.nodes.startInimigos(i))
            self.lista_inimigos.append(novo_inimigo)
            i += 1

    def checkInimigoEvento(self):
        for inimigo in self.lista_inimigos:
            if self.ecoman.colideInimigo(inimigo):
                if self.ecoman.vivo:
                    self.vidas -=  1
                    self.lifesprites.removeImage()
                    raio = self.ecoman.collideRadius
                    self.ecoman.collideRadius = 0
                    if self.vidas == 0:
                        resultado = TelaFinal("derrota", self).executar()
                    else:
                        self.pause.setPause(pauseTime=0.5)  
                inimigo.setSpeed(70)
                threading.Timer(2, self.restaurarVelocidade, args=[inimigo, raio]).start()

    def restaurarVelocidade(self, inimigo, raio):
        inimigo.setSpeed(150)
        self.ecoman.collideRadius = raio

    def hideEntities(self):
        self.ecoman.visible = False
        for inimigo in self.lista_inimigos:
            inimigo.visble = False
    
    def checkQuestEvento(self):
        if self.quest is not None and self.ecoman.collideCheck(self.quest):
            self.quest = None  # Faz o quest sumir da tela
            nova_tela = QuizApp()  # Cria uma nova instância da tela desejada com a janela principal
            acertou = nova_tela.iniciar()  # Armazena o resultado retornado pelo método iniciar
            if acertou:
                self.atualizarPontuacao(1000)
            
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.ecoman.vivo:
                        self.pause.setPause(playerPaused=True)
                    if not self.pause.paused:
                        self.textgroup.hideText()
                    else:
                        self.textgroup.showText(PAUSETXT)

    def checkColetaveisEvento(self):
        coletaveis = self.ecoman.coletar(self.coletaveis.listaColetaveis)
        if coletaveis:
            SOM_COLISAO.play()
            self.coletaveis.numEaten += 1
            self.atualizarPontuacao(coletaveis.points)
            self.coletaveis.listaColetaveis.remove(coletaveis)
            self.textgroup.atualizarLixoRestante(len(self.coletaveis.listaColetaveis) - 1)
            if self.coletaveis.isEmpty():
                self.nextLevel()

    def nextLevel(self):
        if self.level != 4:
            resultado = TelaFinal("vitoria", self).executar()
        else:
            resultado = TelaFinal("fim", self).executar()

    def restartGame(self):
        self.vidas = self.vidas2
        self.segundos = self.segundos2
        self.segundos_aux = 0
        self.score = 0
        self.startGame()

    def atualizarPontuacao(self, points):
        self.score += points
        self.textgroup.atualizarPontuacao(self.score)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        #self.nodes.render(self.screen)
        self.coletaveis.render(self.screen)
        if self.quest is not None:
            self.quest.render(self.screen)
        self.ecoman.render(self.screen)
        for inimigo in self.lista_inimigos:
            inimigo.render(self.screen)
        self.textgroup.render(self.screen)
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = ALTURA_TELA - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x + LARGURA_BLOCO, y - ALTURA_BLOCO))
        pygame.display.update()

if __name__ == "__main__":
    game = Labirinto()
    game.startGame()
    while True:
        game.update()