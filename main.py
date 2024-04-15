import pygame
import sys
from scripts.constantes import *
from labirinto1 import Labirinto  # Importe a classe Labirinto
from scripts.tela_configurações import TelaConfiguracoes
from scripts.seleção_de_fases import TelaSelecaoFases

def main():
    # Inicialização do Pygame
    pygame.init()

    # Definindo cores
    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Tela Inicial")

    # Carregando imagem de fundo
    background_image = pygame.image.load("assets/Imagens/tela_inicial.png").convert()
    background_image = pygame.transform.scale(background_image, (LARGURA_TELA, ALTURA_TELA))

    # Função para desenhar os botões
    def draw_buttons():
        font = pygame.font.Font(None, 36)

        # Botão Jogar
        play_button = font.render("Jogar", True, WHITE)
        play_rect = play_button.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 3))
        screen.blit(play_button, play_rect)

        # Botão Configurações
        settings_button = font.render("Configurações", True, WHITE)
        settings_rect = settings_button.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
        screen.blit(settings_button, settings_rect)

        # Botão Sair
        quit_button = font.render("Sair", True, WHITE)
        quit_rect = quit_button.get_rect(center=(LARGURA_TELA // 2, 2 * ALTURA_TELA // 3))
        screen.blit(quit_button, quit_rect)

        return play_rect, settings_rect, quit_rect

    executando = True
    while executando:
        screen.blit(background_image, (0, 0))  # Desenha o background

        play_rect, settings_rect, quit_rect = draw_buttons()

        # Eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Verificando clique nos botões
                if play_rect.collidepoint(event.pos):
                    tela = TelaSelecaoFases()
                    tela.executar()
                    # labirinto = Labirinto()  
                    # labirinto.startGame()  
                elif settings_rect.collidepoint(event.pos):
                    tela = TelaConfiguracoes()
                    tela.executar()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()
