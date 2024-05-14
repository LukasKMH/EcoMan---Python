import pygame
import numpy as np
import os
from scripts.sprites import Spritesheet, LabirintoSprites, EcomanSprites, ColetavelSprites, InimigoSprites, NumeroVidas
from scripts.constantes import *

def test_spritesheet_creation():
    """
    Testa se a criação do spritesheet é bem-sucedida.
    """
    spritesheet = Spritesheet()
    assert spritesheet is not None

def test_spritesheet_get_image():
    """
    Testa se a obtenção de uma imagem específica do spritesheet é bem-sucedida.
    """
    spritesheet = Spritesheet()
    image = spritesheet.getImage(0, 0, LARGURA_BLOCO, ALTURA_BLOCO)
    assert image is not None

def test_labirinto_sprites_creation():
    """
    Testa se a criação dos sprites do labirinto é bem-sucedida.
    """
    labirinto_sprites = LabirintoSprites("labirinto.txt", "rotacoes.txt")
    assert labirinto_sprites is not None

def test_labirinto_sprites_get_image():
    """
    Testa se a obtenção de um sprite específico do labirinto é bem-sucedida.
    """
    labirinto_sprites = LabirintoSprites("labirinto.txt", "rotacoes.txt")
    image = labirinto_sprites.getImage(0, 0)
    assert image is not None

def test_labirinto_sprites_construct_background():
    """
    Testa a construção do plano de fundo do labirinto.
    """
    labirinto_sprites = LabirintoSprites("labirinto.txt", "rotacoes.txt")
    background = pygame.Surface((800, 600))
    background.fill((0, 0, 0))
    constructed_background = labirinto_sprites.constructBackground(background, 0)
    assert constructed_background is not None

def test_ecoman_sprites_creation():
    """
    Testa a criação dos sprites do Ecoman.
    """
    ecoman_sprites = EcomanSprites(None, "caminho/para/imagens/")
    assert ecoman_sprites is not None

def test_coletavel_sprites_creation():
    """
    Testa a criação dos sprites dos itens coletáveis.
    """
    coletavel_sprites = ColetavelSprites(None, "caminho/para/imagens/")
    assert coletavel_sprites is not None

def test_inimigo_sprites_creation():
    """
    Testa a criação dos sprites dos inimigos.
    """
    inimigo_sprites = InimigoSprites(None, "caminho/para/imagens/")
    assert inimigo_sprites is not None

def test_numerovidas_creation():
    """
    Testa a criação dos sprites do contador de vidas.
    """
    num_vidas = NumeroVidas(3, "caminho/para/imagens/")
    assert num_vidas is not None
