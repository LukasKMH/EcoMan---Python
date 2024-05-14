from scripts.nodes import NodeGroup

def test_nodes_creation():
    '''
    Testa se a criação do grupo de nós é bem-sucedida a partir de um arquivo de mapa.
    '''
    nodes = NodeGroup("assets/mapas/fase1.txt")
    assert nodes is not None

def test_get_node_from_pixels():
    '''
    Testa se é possível obter um nó específico a partir de coordenadas de pixels.
    '''
    nodes = NodeGroup("assets/mapas/fase1.txt")
    node = nodes.getNodeFromPixels(0, 0)
    assert node is not None
    assert node.position.x == 0
    assert node.position.y == 0

def test_get_node_from_tiles():
    '''
    Testa se é possível obter um nó específico a partir de coordenadas de grade.
    '''
    nodes = NodeGroup("assets/mapas/fase1.txt")
    node = nodes.getNodeFromTiles(1, 1) # Supondo que (0,0) é um nó
    assert node is not None
    assert node.position.x == 0
    assert node.position.y == 0

def test_start_temp_node():
    '''
    Testa se é possível obter o nó inicial temporário.
    '''
    nodes = NodeGroup("assets/mapas/fase1.txt")
    start_node = nodes.getStartTempNode()
    assert start_node is not None

def test_start_inimigos():
    '''
    Testa se é possível configurar o nó de início para os inimigos.
    '''
    nodes = NodeGroup("assets/mapas/fase1.txt")
    inimigo_start_node = nodes.startInimigos(1) 
    assert inimigo_start_node is not None

