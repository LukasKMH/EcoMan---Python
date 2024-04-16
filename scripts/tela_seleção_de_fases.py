import pygame
import sys
from pygame.locals import *
from scripts.constantes import *
from scripts.labirinto1 import Labirinto


class TelaSelecaoFases():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Seleção de Fases")
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 36)
        self.texto_titulo = self.fonte.render("Seleção de Fases", True, BRANCO)
        self.botao_voltar_rect = pygame.Rect(10, 10, 30, 30)
        self.botoes_fases = []
        self.voltar_para_tela_inicial = False  # Variável de instância para controlar a mudança de tela

        # Posição dos elementos
        self.texto_titulo_x = LARGURA_TELA // 2
        self.texto_titulo_y = 50
        self.botoes_x = LARGURA_TELA // 2 - 100
        self.botoes_y = 150
        self.espaco_botoes = 60
        self.total_fases = 5

        # Tamanho e posição do retângulo que engloba os botões
        self.retangulo_botoes_width = 300
        self.retangulo_botoes_height = self.total_fases * self.espaco_botoes
        self.retangulo_botoes_x = LARGURA_TELA // 2 - self.retangulo_botoes_width // 2
        self.retangulo_botoes_y = self.botoes_y

        # Criação dos botões de seleção de fases dentro do retângulo
        for i in range(1, self.total_fases + 1):
            botao_rect = pygame.Rect(self.retangulo_botoes_x, self.retangulo_botoes_y + (i - 1) * self.espaco_botoes, self.retangulo_botoes_width, 40)
            self.botoes_fases.append(botao_rect)

    def desenhar_tela(self):
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if self.botao_voltar_rect.collidepoint(pos_mouse):
                    return "tela_inicial"
                # Verifica se algum botão de fase foi clicado
                for i, botao in enumerate(self.botoes_fases):
                    if botao.collidepoint(pos_mouse):
                        if i == 0:
                            labirinto = Labirinto()  
                            labirinto.startGame()
                        elif i == 2:
                            print("Ação específica para o botão 3")
                        else:
                            print(f"Botão da fase {i + 1} pressionado.")  # Ação padrão para os outros botões de fase

        self.screen.fill(AZUL)

        # Desenhar retângulo que engloba os botões
        pygame.draw.rect(self.screen, BRANCO, (self.retangulo_botoes_x, self.retangulo_botoes_y, self.retangulo_botoes_width, self.retangulo_botoes_height))

        # Desenhar título
        self.screen.blit(self.texto_titulo, (self.texto_titulo_x - self.texto_titulo.get_width() // 2, self.texto_titulo_y))

        # Desenhar botão de voltar
        pygame.draw.rect(self.screen, BRANCO, self.botao_voltar_rect)

        # Desenhar números para representar as fases nos botões
        for i, botao in enumerate(self.botoes_fases):
            texto_fase = self.fonte.render(str(i + 1), True, PRETO)
            texto_fase_rect = texto_fase.get_rect(center=botao.center)
            self.screen.blit(texto_fase, texto_fase_rect)

            # Desenhar borda ao redor dos botões
            pygame.draw.rect(self.screen, PRETO, botao, 3)

        pygame.display.flip()

    # def executar(self):
    #     while True:
    #         retorno = self.desenhar_tela()
    #         if retorno is not None:
    #             if retorno == "quit":
    #                 pygame.quit()
    #                 sys.exit()
    #             return retorno

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno is not None:
                if retorno == "quit":
                    pygame.quit()
                    sys.exit()
                elif retorno == "tela_inicial":  # Verifica se deve voltar para a tela inicial
                    return "tela_inicial"
