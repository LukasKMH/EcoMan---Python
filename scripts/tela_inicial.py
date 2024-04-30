import pygame
import sys
from pygame.locals import *
from scripts.constantes import *
from scripts.tela_configurações import TelaConfiguracoes
from scripts.tela_seleção_de_fases import TelaSelecaoFases

class TelaInicial:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Tela Inicial")

        # Carregando imagem de fundo
        self.imagem_fundo = pygame.image.load("assets/Imagens/tela_inicial.png").convert()
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (LARGURA_TELA, ALTURA_TELA))

        self.fonte = pygame.font.Font(None, 40)
        self.largura_borda = 2
        self.largura_botao = LARGURA_TELA // 3
        self.altura_botao = ALTURA_TELA // 9
        self.botao_x = LARGURA_TELA // 3
        self.botao_y = ALTURA_TELA // 3
        self.clock = pygame.time.Clock()

        self.volume = 50
        pygame.mixer.music.set_volume(self.volume / 100)
        self.musica_de_fundo = pygame.mixer.music.load("assets/sons/musica_fundo.wav")
        pygame.mixer.music.play()

    def desenhar_botoes(self):
        retangulo_jogar = pygame.Rect(self.botao_x, self.botao_y, self.largura_botao, self.altura_botao)
        pygame.draw.rect(self.tela, BRANCO, retangulo_jogar)
        pygame.draw.rect(self.tela, PRETO, retangulo_jogar, width=self.largura_borda)

        retangulo_configuracoes = pygame.Rect(self.botao_x, self.botao_y + (7 * ALTURA_BLOCO), self.largura_botao, self.altura_botao)
        pygame.draw.rect(self.tela, BRANCO, retangulo_configuracoes)
        pygame.draw.rect(self.tela, PRETO, retangulo_configuracoes, width=self.largura_borda)

        retangulo_sair = pygame.Rect(self.botao_x, self.botao_y + (14 * ALTURA_BLOCO), self.largura_botao, self.altura_botao)
        pygame.draw.rect(self.tela, BRANCO, retangulo_sair)
        pygame.draw.rect(self.tela, PRETO, retangulo_sair, width=self.largura_borda)

        # Desenha os textos dentro dos botões
        botao_jogar = self.fonte.render("Jogar", True, PRETO)
        jogar_rect = botao_jogar.get_rect(center=retangulo_jogar.center)
        self.tela.blit(botao_jogar, jogar_rect)

        botao_configuracoes = self.fonte.render("Configurações", True, PRETO)
        configuracoes_rect = botao_configuracoes.get_rect(center=retangulo_configuracoes.center)
        self.tela.blit(botao_configuracoes, configuracoes_rect)

        botao_sair = self.fonte.render("Sair", True, PRETO)
        sair_rect = botao_sair.get_rect(center=retangulo_sair.center)
        self.tela.blit(botao_sair, sair_rect)

        return jogar_rect, configuracoes_rect, sair_rect

    def desenhar_tela(self):
        self.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                jogar_rect, configuracoes_rect, sair_rect = self.desenhar_botoes()
                if jogar_rect.collidepoint(event.pos):
                    tela_selecao_fases = TelaSelecaoFases()
                    tela_selecao_fases.executar()
                elif configuracoes_rect.collidepoint(event.pos):
                    tela_configuracoes = TelaConfiguracoes()
                    retorno = tela_configuracoes.executar()
                    if retorno == "tela_inicial":
                        continue  # Volta para o início do loop para desenhar a tela inicial novamente
                elif sair_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        self.tela.blit(self.imagem_fundo, (0, 0))  # Desenha o background
        self.desenhar_botoes()

        pygame.display.flip()

    def executar(self):
        while True:
            retorno = self.desenhar_tela()
            if retorno is not None:
                if retorno == "quit":
                    pygame.quit()
                    sys.exit()
                return retorno


# if __name__ == "__main__":
#     tela_inicial = TelaInicial()
#     tela_inicial.executar()
