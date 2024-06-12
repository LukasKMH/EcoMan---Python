import pygame
import numpy as np
import os
from scripts.sprites import Spritesheet, LabirintoSprites, EcomanSprites, ColetavelSprites, InimigoSprites, NumeroVidas
from scripts.constantes import *

SPRITESHEET = Spritesheet()
LABIRINTO_SPRITES = LabirintoSprites("labirinto.txt", "rotacoes.txt")

def test_spritesheet_creation():
    """
    Testa se a criação do spritesheet é bem-sucedida.
    """
    assert SPRITESHEET is not None

def test_spritesheet_get_image():
    """
    Testa se a obtenção de uma imagem específica do spritesheet é bem-sucedida.
    """
    image = SPRITESHEET.getImage(0, 0, LARGURA_BLOCO, ALTURA_BLOCO)
    assert image is not None

def test_labirinto_sprites_creation():
    """
    Testa se a criação dos sprites do labirinto é bem-sucedida.
    """
    assert LABIRINTO_SPRITES is not None

def test_labirinto_sprites_get_image():
    """
    Testa se a obtenção de um sprite específico do labirinto é bem-sucedida.
    """
    image = LABIRINTO_SPRITES.getImage(0, 0)
    assert image is not None

def test_labirinto_sprites_construct_background():
    """
    Testa a construção do plano de fundo do labirinto.
    """
    background = pygame.Surface((800, 600))
    background.fill((0, 0, 0))
    constructed_background = LABIRINTO_SPRITES.construir_fundo(background, 0)
    assert constructed_background is not None

def test_ecoman_sprites_creation():
    """
    Testa a criação dos sprites do Ecoman.
    """
    ecoman_sprites = EcomanSprites(None, "assets/Imagens/ecoman/submarine_cima.png")
    assert ecoman_sprites is not None

def test_coletavel_sprites_creation():
    """
    Testa a criação dos sprites dos itens coletáveis.
    """
    coletavel_sprites = ColetavelSprites(None, "assets/Imagens/coletavel.png")
    assert coletavel_sprites is not None

def test_inimigo_sprites_creation():
    """
    Testa a criação dos sprites dos inimigos.
    """
    inimigo_sprites = InimigoSprites(None, "assets/Imagens/inimigos/tubarao_cima.png")
    assert inimigo_sprites is not None

def test_numerovidas_creation():
    """
    Testa a criação dos sprites do contador de vidas.
    """
    num_vidas = NumeroVidas(3, "assets/Imagens/vida.png")
    assert num_vidas is not None
