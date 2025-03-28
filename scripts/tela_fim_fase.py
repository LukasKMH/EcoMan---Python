import pygame
import sys
from pygame.locals import *
from scripts.constantes import *

LARGURA_BORDA = 2
LARGURA_BOTAO = LARGURA_BLOCO * 15
ALTURA_BOTAO = ALTURA_TELA // 9
BOTAO_X = LARGURA_BLOCO * 5
BOTAO_Y = ALTURA_BLOCO * 14

class TelaFinal:
    def __init__(self, outcome, tela_chamadora):
        pygame.init()
        self.tela_chamadora = tela_chamadora
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Tela de Vitória")
        self.outcome = outcome
        self.imagem = pygame.image.load("./assets/Imagens/feliz.png") if self.outcome == "vitoria" or self.outcome == "fim" else pygame.image.load("./assets/Imagens/triste.png")
        self.imagem_rect = self.imagem.get_rect()
        self.imagem_rect.center = (LARGURA_TELA // 2 + 200, ALTURA_TELA // 2)
        self.clock = pygame.time.Clock()
        
        # Defina os retângulos dos botões como atributos da classe
        self.retangulo_avancar = pygame.Rect(BOTAO_X, BOTAO_Y, LARGURA_BOTAO, ALTURA_BOTAO)
        self.retangulo_mudar_fase = pygame.Rect(BOTAO_X, BOTAO_Y, LARGURA_BOTAO, ALTURA_BOTAO)

    def desenhar_tela(self):
        self.clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            elif event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.retangulo_mudar_fase.collidepoint(pos_mouse):
                    from scripts.tela_seleção_de_fases import TelaSelecaoFases
                    from scripts.tela_inicial import TelaInicial
                    TelaInicial().executar()
                elif self.retangulo_avancar.collidepoint(pos_mouse) and self.outcome == "vitoria":
                    from scripts.labirinto import Labirinto
                    levels = {
                        1: ("fase2.txt", "fase2_rotacao.txt", 2, 4, 90, 2),
                        2: ("fase3.txt", "fase3_rotacao.txt", 3, 3, 80, 3),
                        3: ("fase4.txt", "fase4_rotacao.txt", 4, 3, 70, 3)
                    }
                    mapa, rotacao, *params = levels.get(self.tela_chamadora.level, (None,)*6)
                    if mapa:
                        Labirinto(f"assets/mapas/{mapa}", f"assets/mapas/{rotacao}", *params).iniciar_jogo()
                elif self.retangulo_avancar.collidepoint(pos_mouse) and self.outcome == "derrota":
                    self.tela_chamadora.restartGame()

                        
        self.tela.fill(AZUL)
        self.tela.blit(self.imagem, self.imagem_rect)
        self.desenhar_texto()
        self.desenhar_botoes()
        pygame.display.update()

    def desenhar_texto(self):
        font = pygame.font.Font(None, 70)
        if self.outcome == "vitoria":
            texto = "Você ganhou!"
        elif self.outcome == "derrota":
            texto = "Que pena!"
        else:
            font = pygame.font.Font(None, 50)
            texto = "Você terminou o jogo!"

        texto_surface = font.render(texto, True, PRETO)  
        texto_rect = texto_surface.get_rect()
        texto_rect.center = (LARGURA_BLOCO * 13, ALTURA_BLOCO * 10)
        self.tela.blit(texto_surface, texto_rect)

    def desenhar_botoes(self):
        font = pygame.font.Font(None, 40)

        # Desenha os botões
        if self.outcome != "fim":
            self.retangulo_mudar_fase = pygame.Rect(BOTAO_X, BOTAO_Y + (6 * ALTURA_BLOCO), LARGURA_BOTAO, ALTURA_BOTAO)
            pygame.draw.rect(self.tela, BRANCO, self.retangulo_avancar)
            pygame.draw.rect(self.tela, PRETO, self.retangulo_avancar, width=LARGURA_BORDA)

        pygame.draw.rect(self.tela, BRANCO, self.retangulo_mudar_fase)
        pygame.draw.rect(self.tela, PRETO, self.retangulo_mudar_fase, width=LARGURA_BORDA)

        # Desenha os textos dentro dos botões
        if self.outcome == "vitoria":
            texto_avancar = font.render("Avançar", True, PRETO)
        elif self.outcome == "derrota":
            texto_avancar = font.render("Recomeçar", True, PRETO)
        else:
            texto_avancar = font.render("", True, PRETO)
        texto_mudar_fase = font.render("Tela inicial", True, PRETO)

        avancar_rect = texto_avancar.get_rect(center=self.retangulo_avancar.center)
        mudar_fase_rect = texto_mudar_fase.get_rect(center=self.retangulo_mudar_fase.center)

        if self.outcome != "fim":
            self.tela.blit(texto_avancar, avancar_rect)
        self.tela.blit(texto_mudar_fase, mudar_fase_rect)

        return avancar_rect, mudar_fase_rect

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno is not None:
                if retorno == "quit":
                    pygame.quit()
                    sys.exit()
                return retorno