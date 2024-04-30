import pygame
import sys
from pygame.locals import *
from scripts.constantes import *

class TelaConfiguracoes:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Configurações")
        self.clock = pygame.time.Clock()
        self.fonte1 = pygame.font.Font(None, 72)
        self.fonte2 = pygame.font.Font(None, 44)

        self.texto_titulo = self.fonte1.render("Configurações", True, PRETO)
        self.texto_volume = self.fonte2.render("Volume:", True, PRETO)

        # Posição dos elementos
        self.texto_titulo_x = LARGURA_TELA // 2
        self.texto_titulo_y = 150
        self.texto_volume_x = LARGURA_TELA // 2 - LARGURA_BLOCO * 3
        self.texto_volume_y = ALTURA_BLOCO * 14 

        self.volume_bar_width = 200
        self.volume_bar_height = 10
        self.botao_voltar_rect = pygame.Rect(10, 10, 30, 30)
        
        # Botões para aumentar e diminuir o volume (agora redondos)
        self.botao_aumentar = (LARGURA_TELA // 2 + LARGURA_BLOCO * 10, ALTURA_BLOCO * 18)
        self.botao_diminuir = (LARGURA_TELA // 2 - LARGURA_BLOCO * 10, ALTURA_BLOCO * 18)
        self.botao_raio = 20

        # Volume
        self.volume = 50  # Defina o volume inicial em uma escala de 0 a 100
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
                elif self.distancia(pos_mouse, self.botao_aumentar) <= self.botao_raio:
                    self.aumentar_volume()
                elif self.distancia(pos_mouse, self.botao_diminuir) <= self.botao_raio:
                    self.diminuir_volume()

        self.tela.fill(AZUL)

        # Desenhar textos
        self.tela.blit(self.texto_titulo, (self.texto_titulo.get_width() // 2 + 2 * LARGURA_BLOCO, ALTURA_BLOCO * 3))
        self.tela.blit(self.texto_volume, (self.texto_volume_x, self.texto_volume_y))

        # Desenhar barra de volume
        volume_bar_x = LARGURA_TELA // 2 - self.volume_bar_width // 2
        volume_bar_y = ALTURA_TELA // 2 - self.volume_bar_height // 2
        pygame.draw.rect(self.tela, BRANCO, (volume_bar_x, volume_bar_y, self.volume_bar_width, self.volume_bar_height))
       
        # Bolinha de volume
        volume_proporcao = self.volume / self.volume_maximo
        volume_bola_x = volume_bar_x + (self.volume_bar_width * volume_proporcao)
        volume_bola_y = volume_bar_y + self.volume_bar_height // 2
        pygame.draw.circle(self.tela, AMARELO, (int(volume_bola_x), volume_bola_y), 8)

        # Botão voltar
        self.botao_voltar_rect = pygame.Rect(LARGURA_BLOCO * 3 - 30, ALTURA_BLOCO * 3 - 30, 60, 60)  
        pygame.draw.rect(self.tela, AZUL, self.botao_voltar_rect, border_radius=25)
        icone_voltar = pygame.image.load("assets/Imagens/voltar.png").convert_alpha() 
        icone_rect = icone_voltar.get_rect(center=self.botao_voltar_rect.center)
        self.tela.blit(icone_voltar, icone_rect)

        # Desenhar botões de aumentar e diminuir volume (redondos)
        pygame.draw.circle(self.tela, AZUL_CLARO, self.botao_aumentar, self.botao_raio)
        pygame.draw.circle(self.tela, AZUL_CLARO, self.botao_diminuir, self.botao_raio)

        # Texto nos botões
        texto_mais = self.fonte2.render("+", True, PRETO)
        texto_menos = self.fonte2.render("-", True, PRETO)
        self.tela.blit(texto_mais, (self.botao_aumentar[0] - texto_mais.get_width() // 2, self.botao_aumentar[1] - texto_mais.get_height() // 2))
        self.tela.blit(texto_menos, (self.botao_diminuir[0] - texto_menos.get_width() // 2, self.botao_diminuir[1] - texto_menos.get_height() // 2))

        pygame.display.flip()

    def distancia(self, pos1, pos2):
        """Calcula a distância entre duas posições."""
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

    def aumentar_volume(self):
        """Aumenta o volume em 10%."""
        self.volume = min(self.volume_maximo, self.volume + 10)
        pygame.mixer.music.set_volume(self.volume / 100)

    def diminuir_volume(self):
        """Diminui o volume em 10%."""
        self.volume = max(self.volume_minimo, self.volume - 10)
        pygame.mixer.music.set_volume(self.volume / 100)

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno is not None:
                if retorno == "quit":
                    pygame.quit()
                    sys.exit()
                return retorno
