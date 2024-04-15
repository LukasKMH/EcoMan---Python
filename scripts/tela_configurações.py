import pygame
import sys
from pygame.locals import *
from scripts.constantes import *

class TelaConfiguracoes:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Configurações")
        self.clock = pygame.time.Clock()

        # Cores
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.AMARELO = (255, 255, 0)

        # Fonte
        self.fonte = pygame.font.Font(None, 36)

        # Textos e botões
        self.texto_titulo = self.fonte.render("Configurações", True, self.PRETO)
        self.texto_volume = self.fonte.render("Volume:", True, self.PRETO)

        # Posição dos elementos
        self.texto_titulo_x = LARGURA_TELA // 2
        self.texto_titulo_y = 150
        self.texto_volume_x = LARGURA_TELA // 2
        self.texto_volume_y = 220

        self.volume_bar_width = 200
        self.volume_bar_height = 10
        self.botao_voltar_rect = pygame.Rect(10, 10, 30, 30)

        # Volume
        self.volume = 50
        self.volume_maximo = 100
        self.volume_minimo = 0

    def desenhar_tela(self):
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            elif event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar_rect.collidepoint(pos_mouse):
                    return "tela_inicial"

        self.screen.fill(AZUL)

        # Desenhar textos
        self.screen.blit(self.texto_titulo, (self.texto_titulo_x, self.texto_titulo_y))
        self.screen.blit(self.texto_volume, (self.texto_volume_x, self.texto_volume_y))

        # Desenhar barra de volume
        volume_bar_x = LARGURA_TELA // 2 - self.volume_bar_width // 2
        volume_bar_y = ALTURA_TELA // 2 - self.volume_bar_height // 2
        pygame.draw.rect(self.screen, self.BRANCO, (volume_bar_x, volume_bar_y, self.volume_bar_width, self.volume_bar_height))
        # Bolinha de volume
        volume_proporcao = self.volume / self.volume_maximo
        volume_bola_x = volume_bar_x + (self.volume_bar_width * volume_proporcao)
        volume_bola_y = volume_bar_y + self.volume_bar_height // 2
        pygame.draw.circle(self.screen, self.AMARELO, (int(volume_bola_x), volume_bola_y), 8)

        # Desenhar botão de voltar
        pygame.draw.rect(self.screen, self.BRANCO, self.botao_voltar_rect)
        pygame.display.flip()

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno is not None:
                if retorno == "quit":
                    pygame.quit()
                    sys.exit()
                return retorno
