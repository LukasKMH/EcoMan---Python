import pygame
import threading
from pygame.locals import *
from constantes import *
from ecoman import Ecoman
from nodes import NodeGroup
from coletaveis import GrupoColetaveis
from inimigo import Inimigo
from quest import Quest
from pause import Pause

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(TAMANHO_TELA, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.quest = None
        self.pause = Pause(False)

    def setBackground(self):
        self.background = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.background.fill(PRETO)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("fase2.txt") 
        self.ecoman = Ecoman(self.nodes.getStartTempNode())
        self.coletaveis = GrupoColetaveis("fase2.txt")
        self.lista_inimigos = []
        self.gerarInimigos(3)

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.coletaveis.update(dt)
        if not self.pause.paused:
            self.ecoman.update(dt)
            for inimigo in self.lista_inimigos:
                inimigo.update(dt)
            if self.quest is not None:
                self.quest.update(dt)
            self.checkPelletEvents()
            self.checkInimigoEvento()
            self.checkQuestEvento()
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def gerarInimigos(self, quantidade):
        for _ in range(quantidade):
            novo_inimigo = Inimigo(self.nodes.getStartTempNode())  # Crie um novo inimigo
            self.lista_inimigos.append(novo_inimigo)  # Adicione o inimigo à lista

    def checkInimigoEvento(self):
        for inimigo in self.lista_inimigos:
            if self.ecoman.colideInimigo(inimigo):

                # self.ecoman.visible = False
                # inimigo.visible = False
                # self.pause.setPause(pauseTime=1, func=self.showEntities)

                inimigo.setSpeed(500)
                # Inicia um temporizador para restaurar a velocidade após 2 segundos
                threading.Timer(2, self.restaurarVelocidade, args=[inimigo]).start()


    # Deixar inimigos e o ecoman visiveis ou nao
    # def showEntities(self):
    #     self.ecoman.visible = True
    #     for inimigo in self.lista_inimigos:
    #         inimigo.visble = True

    # def hideEntities(self):
    #     self.ecoman.visible = False
    #     for inimigo in self.lista_inimigos:
    #         inimigo.visble = False
    
    def restaurarVelocidade(self, inimigo):
        # Retorna a velocidade do inimigo ao normal
        inimigo.setSpeed(100)

    def checkQuestEvento(self):
        if self.coletaveis.numEaten == 1:
            if self.quest is None:
                self.quest = Quest(self.nodes.getStartTempNode())
        if self.quest is not None:
            if self.ecoman.collideCheck(self.quest):
                self.quest = None
            elif self.quest.destroy:
                self.quest = None
                
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.pause.setPause(playerPaused=True)
                    # if not self.pause.paused:
                    #     self.showEntities()
                    # else:
                    #     self.hideEntities()

    def checkPelletEvents(self):
        coletaveis = self.ecoman.eatPellets(self.coletaveis.listaColetaveis)
        if coletaveis:
            self.coletaveis.numEaten += 1
            self.coletaveis.listaColetaveis.remove(coletaveis)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.coletaveis.render(self.screen)
        if self.quest is not None:
            self.quest.render(self.screen)
        self.ecoman.render(self.screen)
        for inimigo in self.lista_inimigos:
            inimigo.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
