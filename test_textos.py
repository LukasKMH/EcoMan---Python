from scripts.texto import Text, TextGroup
from scripts.constantes import *

def test_textgroup_creation():
    """
    Testa se a criação de um grupo de texto é bem-sucedida.
    """
    textgroup = TextGroup()
    assert textgroup is not None

def test_textgroup_add_and_remove_text():
    """
    Testa a adição e remoção de texto em um grupo de texto.
    """
    textgroup = TextGroup()
    text_id = textgroup.addText("Test", BRANCO, 100, 100, 20)
    assert text_id is not None
    textgroup.removeText(text_id)
    assert text_id not in textgroup.alltext.keys()

def test_textgroup_update():
    """
    Testa se a atualização de um grupo de texto ocorre sem erros.
    """
    textgroup = TextGroup()
    textgroup.update(0.1)

def test_textgroup_format_time():
    """
    Testa a formatação do tempo em um grupo de texto.
    """
    textgroup = TextGroup()
    formatted_time = textgroup.formatarTempo(55)
    assert formatted_time == "00:55"

