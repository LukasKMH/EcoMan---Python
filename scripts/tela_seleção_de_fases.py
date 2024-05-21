import pygame
import sys
from pygame.locals import *
from scripts.constantes import *
from scripts.labirinto import Labirinto

class TelaSelecaoFases():
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Seleção de Fases")
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 72) 
        self.texto_titulo = self.fonte.render("Seleção de Fases", True, PRETO)

        self.botao_voltar_rect = pygame.Rect(10, 10, 80, 40)
        self.botoes_fases = []
        self.voltar_para_tela_inicial = False

        # Posição dos elementos
        self.largura_botao = LARGURA_BLOCO * 6
        self.altura_botao = ALTURA_BLOCO * 6
        self.espaco_botoes = LARGURA_BLOCO * 8.7
        self.total_fases = 4

        # Criação dos botões de seleção de fases
        for i in range(self.total_fases):
            botao_rect = pygame.Rect(0, 0, self.largura_botao, self.altura_botao)
            self.botoes_fases.append(botao_rect)

    def desenhar_tela(self):
        self.clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "quit"
            elif evento.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar_rect.collidepoint(pos_mouse):
                    return "tela_inicial"
                for i, botao in enumerate(self.botoes_fases):
                    if botao.collidepoint(pos_mouse):
                        pygame.mixer.music.stop()
                        if i == 0:
                            labirinto = Labirinto("assets/mapas/fase1.txt", "assets/mapas/fase1_rotacao.txt", 1, 4, 100, 2)  
                        elif i == 1:
                            labirinto = Labirinto("assets/mapas/fase2.txt", "assets/mapas/fase2_rotacao.txt", 2, 4, 90, 2)  
                        elif i == 2:
                            labirinto = Labirinto("assets/mapas/fase3.txt", "assets/mapas/fase3_rotacao.txt", 3, 3, 80, 3)  
                        elif i == 3:
                            labirinto = Labirinto("assets/mapas/fase4.txt", "assets/mapas/fase4_rotacao.txt", 4, 3, 70, 3)  
                        labirinto.iniciar_jogo()

        self.tela.fill(AZUL)

        # Desenhar título
        self.tela.blit(self.texto_titulo, (self.texto_titulo.get_width() // 2 - 2 * LARGURA_BLOCO, ALTURA_BLOCO * 3))

        # Botão voltar
        self.botao_voltar_rect = pygame.Rect(LARGURA_BLOCO * 3 - 30, ALTURA_BLOCO * 3 - 30, 60, 60)  
        pygame.draw.rect(self.tela, AZUL, self.botao_voltar_rect, border_radius=25)
        icone_voltar = pygame.image.load("assets/Imagens/voltar.png").convert_alpha() 
        icone_rect = icone_voltar.get_rect(center=self.botao_voltar_rect.center)
        self.tela.blit(icone_voltar, icone_rect)

        # Desenhar retângulo azul claro para os botões de fases
        retangulo_botoes = pygame.Rect(LARGURA_BLOCO * 5, ALTURA_BLOCO * 10, LARGURA_TELA - (LARGURA_BLOCO * 10), ALTURA_BLOCO * 15 )
        pygame.draw.rect(self.tela, AZUL_CLARO, retangulo_botoes, border_radius=45)
        pygame.draw.rect(self.tela, PRETO, retangulo_botoes, 2, border_radius=45)

        # Ajustar a posição dos botões de acordo com o retângulo
        for i, botao in enumerate(self.botoes_fases):
            botao.x = retangulo_botoes.x + (LARGURA_BLOCO * 2) + i * self.espaco_botoes
            botao.y = retangulo_botoes.y + ALTURA_BLOCO * 2
            pygame.draw.rect(self.tela, BRANCO, botao, border_radius=45)
            pygame.draw.rect(self.tela, PRETO, botao, 2, border_radius=45)

            # Calcular as coordenadas para o centro do botão
            centro_x = botao.x + botao.width // 2
            centro_y = botao.y + botao.height // 2

            # Renderizar e desenhar o número da fase no centro do botão
            numero_fase = self.fonte.render(str(i + 1), True, AZUL)
            texto_rect = numero_fase.get_rect(center=(centro_x, centro_y))
            self.tela.blit(numero_fase, texto_rect)

        pygame.display.flip()

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno is not None:
                if retorno == "quit":
                    pygame.quit()
                    sys.exit()
                elif retorno == "tela_inicial": 
                    return "tela_inicial"
