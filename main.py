import pygame
from pygame.locals import *
from constantes import *
from ecoman import Ecoman
from nodes import NodeGroup
from coletaveis import GrupoColetaveis

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(TAMANHO_TELA, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()

    def setBackground(self):
        self.background = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.background.fill(PRETO)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("fase2.txt") 
        self.ecoman = Ecoman(self.nodes.getStartTempNode())
        self.coletaveis = GrupoColetaveis("fase2.txt")

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.ecoman.update(dt)
        self.coletaveis.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def checkPelletEvents(self):
        coletaveis = self.ecoman.eatPellets(self.coletaveis.listaColetaveis)
        if coletaveis:
            self.coletaveis.numEaten += 1
            self.coletaveis.listaColetaveis.remove(coletaveis)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.coletaveis.render(self.screen)
        self.ecoman.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
