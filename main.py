import pygame
from pygame.locals import *
from scripts.tela_inicial import TelaInicial
from scripts.tela_seleção_de_fases import TelaSelecaoFases
from scripts.tela_configurações import TelaConfiguracoes
from scripts.labirinto import Labirinto

class ControladorTelas:
    """Classe que controla as telas do jogo. Possui uma variável que armazena a tela atual
    e um método que inicia o jogo. As telas se comunicam a partir de um retorno de string entre elas."""
    def __init__(self):
        pygame.init()
        self.tela_atual = None
    
    def iniciar(self):
        """Enquanto a tela atual for diferente de None, o jogo continua rodando. Cada tela é instanciada"""
        while True:
            if self.tela_atual is None or self.tela_atual == "tela_inicial":
                tela_inicial = TelaInicial()
                self.tela_atual = tela_inicial.executar()

            elif self.tela_atual == "selecao_fases":
                tela_selecao_fases = TelaSelecaoFases()
                self.tela_atual = tela_selecao_fases.executar()

            elif self.tela_atual == "configuracoes":
                tela_configuracoes = TelaConfiguracoes()
                self.tela_atual = tela_configuracoes.executar()

            elif self.tela_atual == "fase1":
                labirinto = Labirinto()
                self.tela_atual = labirinto.iniciar_jogo()

if __name__ == "__main__":
    controlador = ControladorTelas()
    controlador.iniciar()
