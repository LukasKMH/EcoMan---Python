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
#from tela_fim_fase import TelaFinal

from scripts.inimigo2 import GrupoInimigos

class Labirinto(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(TAMANHO_TELA, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.quest = None
        self.pause = Pause(False)
        self.level = 1
        self.vidas = 4
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = NumeroVidas(self.vidas, "assets/Imagens/vida.png")


    def setBackground(self):
        self.background = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.background.fill(AZUL)

    def startGame(self):
        self.setBackground()
        self.mazesprites = LabirintoSprites("fase2.txt", "maze1_rotation.txt")
        self.background = self.mazesprites.constructBackground(self.background, self.level%5)
        self.nodes = NodeGroup("fase2.txt") 
        self.ecoman = Ecoman(self.nodes.getStartTempNode())
        self.coletaveis = GrupoColetaveis("fase2.txt")
        self.lista_inimigos = []
        while True:
            self.update()

        #self.gerarInimigos(3)

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.textgroup.update(dt)
        self.coletaveis.update(dt)
        if not self.pause.paused:
            self.ecoman.update(dt)
            for inimigo in self.lista_inimigos:
                inimigo.update(dt)
            if self.quest is not None:
                self.quest.update(dt)
            self.checkPelletEvents()  # Verificar se algum coletável foi consumido
            self.checkInimigoEvento()
            self.checkQuestEvento()
            # Contar o número de coletáveis restantes após a verificação
            self.textgroup.atualizarLixoRestante(len(self.coletaveis.listaColetaveis) - 1)
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
        
                if self.pacman.alive:
                    self.lives -=  1
                    self.lifesprites.removeImage()
                    self.pacman.die()
                    self.ghosts.hide()
                    if self.lives <= 0:
                        self.textgroup.showText(GAMEOVERTXT)
                        self.pause.setPause(pauseTime=3, func=self.restartGame)
                    else:
                        self.pause.setPause(pauseTime=3, func=self.resetLevel)


                # inimigo.setSpeed(500)
                # # Inicia um temporizador para restaurar a velocidade após 2 segundos
                # threading.Timer(2, self.restaurarVelocidade, args=[inimigo]).start()

    # Deixar inimigos e o ecoman visiveis ou nao
    def showEntities(self):
        self.ecoman.visible = True
        for inimigo in self.lista_inimigos:
            inimigo.visble = True

    def hideEntities(self):
        self.ecoman.visible = False
        for inimigo in self.lista_inimigos:
            inimigo.visble = False
    
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
                    if self.ecoman.vivo:
                        self.pause.setPause(playerPaused=True)
                    if not self.pause.paused:
                        self.textgroup.hideText()
                    #     self.showEntities()
                    else:
                        self.textgroup.showText(PAUSETXT)
                    #     self.hideEntities()

    def checkPelletEvents(self):
        coletaveis = self.ecoman.eatPellets(self.coletaveis.listaColetaveis)
        if coletaveis:
            self.coletaveis.numEaten += 1
            self.atualizarPontuacao(coletaveis.points)
            self.coletaveis.listaColetaveis.remove(coletaveis)
            # Atualizar o número de coletáveis restantes
            self.textgroup.atualizarLixoRestante(len(self.coletaveis.listaColetaveis) - 1)
            if self.coletaveis.isEmpty():
                #resultado = TelaFinal("vitoria").executar()
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)


    def nextLevel(self):
        self.showEntities() 
        self.level += 1
        self.pause.paused = True
        self.startGame()

    def restartGame(self):
        self.lives = 4
        self.level = 1
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.atualizarPontuacao(self.score)
        self.textgroup.atualizarLixoRestante(len(self.coletaveis.listaColetaveis) - 1)
        self.textgroup.showText(PRONTOTXT)
        self.lifesprites.resetLives(self.lives)

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(PRONTOTXT)

    def atualizarPontuacao(self, points):
        self.score += points
        self.textgroup.atualizarPontuacao(self.score)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.coletaveis.render(self.screen)
        if self.quest is not None:
            self.quest.render(self.screen)
        self.ecoman.render(self.screen)
        for inimigo in self.lista_inimigos:
            inimigo.render(self.screen)
        #self.lista_inimigos.render(self.screen)
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