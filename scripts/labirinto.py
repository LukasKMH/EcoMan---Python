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
from scripts.texto import GrupoTexto
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
        self.textgroup = GrupoTexto()
        self.nodes = NodeGroup(self.mapa)
        self.lista_inimigos = []
        self.gerar_inimigos(numero_inimigos)
        self.lifesprites = NumeroVidas(self.vidas, "assets/Imagens/vida.png")

    def definir_fundo(self):
        self.background = pygame.surface.Surface(TAMANHO_TELA).convert()
        self.background.fill(AZUL)

    def iniciar_jogo(self):
        self.definir_fundo()
        self.quest = Quest(self.nodes.no_inicial(6))
        self.mazesprites = LabirintoSprites(self.mapa, self.mapa_rotacao)
        self.background = self.mazesprites.construir_fundo(self.background)
        self.ecoman = Ecoman(self.nodes.no_inicial(0))
        self.coletaveis = GrupoColetaveis(self.mapa)
        self.textgroup.atualizar_pontuacao(self.score)
        self.textgroup.atualizar_lixo(len(self.coletaveis.lista_coletaveis) - 1)
        self.lifesprites.reset_vidas(self.vidas)
        self.atualizar_tempo()
        while True:
            self.update()

    def update(self):
        dt = self.clock.tick(60) / 1000.0
        self.segundos_aux += 1
        self.textgroup.update(dt)
        if not self.pause.pausado:
            self.ecoman.update(dt)
            for inimigo in self.lista_inimigos:
                inimigo.update(dt)
            if self.quest is not None:
                self.quest.update(dt)
            self.verificar_evento_coletavel()
            if self.ecoman.raio_colisao != 0:
                self.verficiar_evento_inimigo()
            self.verificar_evento_quest()
            self.textgroup.atualizar_lixo(len(self.coletaveis.lista_coletaveis) - 1)
            if self.segundos_aux >= 60:
                self.segundos_aux = 0
                self.segundos -= 1
                self.atualizar_tempo()

        depois_pausado = self.pause.update(dt)
        if depois_pausado is not None:
            depois_pausado()
        self.verificar_evento()
        self.render()

    def atualizar_tempo(self):
        if not self.textgroup.atualizar_tempo(self.segundos):
            TelaFinal("derrota", self).executar()
        
    def gerar_inimigos(self, quantidade):
        for _ in range(quantidade):
            i = 22
            novo_inimigo = Inimigo(self.nodes.no_inicial(i))
            self.lista_inimigos.append(novo_inimigo)
            i += 1

    def verficiar_evento_inimigo(self):
        for inimigo in self.lista_inimigos:
            if self.ecoman.colideInimigo(inimigo):
                if self.ecoman.vivo:
                    self.vidas -=  1
                    self.lifesprites.remover_imagem()
                    raio = self.ecoman.raio_colisao
                    self.ecoman.raio_colisao = 0
                    if self.vidas == 0:
                        TelaFinal("derrota", self).executar()
                    else:
                        self.pause.pausar(tempo_pausa=0.5)  
                inimigo.definir_velocidade(10)
                threading.Timer(2, self.restaurar_velocidade, args=[inimigo, raio]).start()

    def restaurar_velocidade(self, inimigo, raio):
        inimigo.definir_velocidade(150)
        self.ecoman.raio_colisao = raio
    
    def verificar_evento_quest(self):
        if self.quest is not None and self.ecoman.collideCheck(self.quest):
            self.quest = None  
            nova_tela = QuizApp() 
            acertou = nova_tela.iniciar()  
            if acertou:
                self.atualizar_pontuacao(1000)
            
    def verificar_evento(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                if self.ecoman.vivo:
                    self.pause.pausar()
                if self.pause.pausado:
                    self.textgroup.mostrar_texto(PAUSETXT)
                else:
                    self.textgroup.esconder_texto()

    def verificar_evento_coletavel(self):
        coletaveis = self.ecoman.coletar(self.coletaveis.lista_coletaveis)
        if coletaveis:
            SOM_COLISAO.play()
            self.coletaveis.coletados += 1
            self.atualizar_pontuacao(coletaveis.pontuacao)
            self.coletaveis.lista_coletaveis.remove(coletaveis)
            self.textgroup.atualizar_lixo(len(self.coletaveis.lista_coletaveis) - 1)
            if self.coletaveis.esta_vazio():
                self.proximo_level()

    def proximo_level(self):
        TelaFinal("vitoria" if self.level != 4 else "fim", self).executar()

    def restart_game(self):
        self.vidas = self.vidas2
        self.segundos = self.segundos2
        self.segundos_aux = 0
        self.score = 0
        self.iniciar_jogo()

    def atualizar_pontuacao(self, pontuacao):
        self.score += pontuacao
        self.textgroup.atualizar_pontuacao(self.score)

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
    game.iniciar_jogo()
    while True:
        game.update()