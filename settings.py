# Abre o arquivo "levelMap.txt" em modo de leitura
levelmap = open("mapa/levelMap.txt", 'r')

# Função para ler e retornar o mapa do nível
def returnLevelMap(file):
    levelMap = []
    for line in file:
        line = line.strip()
        levelMap.append(line)
    return levelMap

# Chama a função para obter o mapa do nível
level_map = returnLevelMap(levelmap)

# Configurações da tela
tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size  # Calcula a altura da tela com base no número de linhas no mapa e no tamanho do tile

# Fechamento do arquivo após usá-lo
levelmap.close()
