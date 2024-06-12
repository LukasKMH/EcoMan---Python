from scripts.nodes import NodeGroup

NODES = NodeGroup("assets/mapas/fase1.txt")
def test_nodes_creation():
    '''
    Testa se a criação do grupo de nós é bem-sucedida a partir de um arquivo de mapa.
    '''
    assert NODES is not None

def test_get_node_from_pixels():
    '''
    Testa se é possível obter um nó específico a partir de coordenadas de pixels.
    '''
    node = NODES.obter_no_pixel(0, 0)
    assert node is not None
    assert node.position.x == 0
    assert node.position.y == 0

def test_get_node_from_tiles():
    '''
    Testa se é possível obter um nó específico a partir de coordenadas de grade.
    '''
    node = NODES.obter_no_tiles(1, 1) # Supondo que (0,0) é um nó
    assert node is not None
    assert node.position.x == 0
    assert node.position.y == 0

def test_start_temp_node():
    '''
    Testa se é possível obter o nó inicial temporário.
    '''
    start_node = NODES.getStartTempNode()
    assert start_node is not None

def test_start_inimigos():
    '''
    Testa se é possível configurar o nó de início para os inimigos.
    '''
    inimigo_start_node = NODES.no_inicial(1) 
    assert inimigo_start_node is not None

