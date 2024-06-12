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
        for _ in range(self.total_fases):
            botao_rect = pygame.Rect(0, 0, self.largura_botao, self.altura_botao)
            self.botoes_fases.append(botao_rect)

    def desenhar_tela(self):
        self.clock.tick(FPS)

        acao = self._tratar_eventos()
        if acao:
            return acao

        self._desenhar_fundo()
        self._desenhar_titulo()
        self._desenhar_botao_voltar()
        self._desenhar_retangulo_botoes()
        self._desenhar_botoes_fases()

        pygame.display.flip()

    def _tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "quit"
            if evento.type == MOUSEBUTTONDOWN:
                return self._tratar_evento_mouse()

    def _tratar_evento_mouse(self):
        pos_mouse = pygame.mouse.get_pos()
        if self.botao_voltar_rect.collidepoint(pos_mouse):
            return "tela_inicial"

        fase_parametros = [
            ("assets/mapas/fase1.txt", "assets/mapas/fase1_rotacao.txt", 1, 4, 100, 2),
            ("assets/mapas/fase2.txt", "assets/mapas/fase2_rotacao.txt", 2, 4, 90, 2),
            ("assets/mapas/fase3.txt", "assets/mapas/fase3_rotacao.txt", 3, 3, 80, 3),
            ("assets/mapas/fase4.txt", "assets/mapas/fase4_rotacao.txt", 4, 3, 70, 3)
        ]

        for i, botao in enumerate(self.botoes_fases):
            if botao.collidepoint(pos_mouse):
                pygame.mixer.music.stop()
                parametros = fase_parametros[i]
                labirinto = Labirinto(*parametros)
                labirinto.iniciar_jogo()
                break

    def _desenhar_fundo(self):
        self.tela.fill(AZUL)

    def _desenhar_titulo(self):
        self.tela.blit(self.texto_titulo, (self.texto_titulo.get_width() // 2 - 2 * LARGURA_BLOCO, ALTURA_BLOCO * 3))

    def _desenhar_botao_voltar(self):
        self.botao_voltar_rect = pygame.Rect(LARGURA_BLOCO * 3 - 30, ALTURA_BLOCO * 3 - 30, 60, 60)
        pygame.draw.rect(self.tela, AZUL, self.botao_voltar_rect, border_radius=25)
        icone_voltar = pygame.image.load("assets/Imagens/voltar.png").convert_alpha()
        icone_rect = icone_voltar.get_rect(center=self.botao_voltar_rect.center)
        self.tela.blit(icone_voltar, icone_rect)

    def _desenhar_retangulo_botoes(self):
        retangulo_botoes = pygame.Rect(LARGURA_BLOCO * 5, ALTURA_BLOCO * 10, LARGURA_TELA - (LARGURA_BLOCO * 10), ALTURA_BLOCO * 15)
        pygame.draw.rect(self.tela, AZUL_CLARO, retangulo_botoes, border_radius=45)
        pygame.draw.rect(self.tela, PRETO, retangulo_botoes, 2, border_radius=45)

    def _desenhar_botoes_fases(self):
        retangulo_botoes = pygame.Rect(LARGURA_BLOCO * 5, ALTURA_BLOCO * 10, LARGURA_TELA - (LARGURA_BLOCO * 10), ALTURA_BLOCO * 15)
        for i, botao in enumerate(self.botoes_fases):
            botao.x = retangulo_botoes.x + (LARGURA_BLOCO * 2) + i * self.espaco_botoes
            botao.y = retangulo_botoes.y + ALTURA_BLOCO * 2
            pygame.draw.rect(self.tela, BRANCO, botao, border_radius=45)
            pygame.draw.rect(self.tela, PRETO, botao, 2, border_radius=45)

            centro_x = botao.x + botao.width // 2
            centro_y = botao.y + botao.height // 2

            numero_fase = self.fonte.render(str(i + 1), True, AZUL)
            texto_rect = numero_fase.get_rect(center=(centro_x, centro_y))
            self.tela.blit(numero_fase, texto_rect)


    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno is not None:
                if retorno == "quit":
                    pygame.quit()
                    sys.exit()
                elif retorno == "tela_inicial": 
                    return "tela_inicial"
