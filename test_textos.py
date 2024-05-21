from scripts.texto import Text, GrupoTexto
from scripts.constantes import *

def test_textgroup_creation():
    """
    Testa se a criação de um grupo de texto é bem-sucedida.
    """
    textgroup = GrupoTexto()
    assert textgroup is not None

def test_textgroup_add_and_remove_text():
    """
    Testa a adição e remoção de texto em um grupo de texto.
    """
    textgroup = GrupoTexto()
    text_id = textgroup.adicionar_texto("Test", BRANCO, 100, 100, 20)
    assert text_id is not None
    textgroup.remover_texto(text_id)
    assert text_id not in textgroup.textos.keys()

def test_textgroup_update():
    """
    Testa se a atualização de um grupo de texto ocorre sem erros.
    """
    textgroup = GrupoTexto()
    textgroup.update(0.1)

def test_textgroup_format_time():
    """
    Testa a formatação do tempo em um grupo de texto.
    """
    textgroup = GrupoTexto()
    formatted_time = textgroup.formatar_tempo(55)
    assert formatted_time == "00:55"

