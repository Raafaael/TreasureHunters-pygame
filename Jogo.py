import pygame
import sys
from settings import *
from level import Level
from clouds import Cloud
from ui import UI

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

mapa = pygame.image.load("map.png")
inimigos = 'mapa/level1_enemies.txt'
moedas = 'mapa/level1_coins.txt'
palmeiras = 'mapa/levelPalm.txt'
objetivo = 'mapa/levelGoal.txt'
ondas = "mapa/levelWave.txt"

level = Level(level_map, screen, mapa, inimigos, moedas, palmeiras, objetivo, ondas)

clouds = pygame.sprite.Group()
ui = UI(level.player.sprite)

# Criar várias nuvens com posições e velocidades diferentes
cloud_positions = [(100, 50), (300, 150), (500, 100), (0,50)]
cloud_speeds = [-2, -3, -1]

for pos, speed in zip(cloud_positions, cloud_speeds):
    cloud = Cloud(pos, speed)
    clouds.add(cloud)

# Variável para controlar se o jogo está no menu
in_menu = True

# Carregar a imagem de fundo
background_image = pygame.image.load("menu_logo.png")
background_image = pygame.transform.scale(background_image, (background_image.get_width()/1.6, background_image.get_height()/1.5))
background_rect = background_image.get_rect(center=(screen_width // 2, screen_height // 2))

# Carregar a música
pygame.mixer.music.load('music/music_menu.wav')
pygame.mixer.music.set_volume(0.2)  # Defina o volume desejado entre 0.0 e 1.0
pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente


# Mensagem do menu
font = pygame.font.Font(None, 36)

while in_menu:

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif keys[pygame.K_RETURN]:
            in_menu = False

    screen.blit(background_image, background_rect)  # Desenha a imagem de fundo

    pygame.display.update()
    clock.tick(60)

# Parar a música quando não for mais necessária
pygame.mixer.music.stop()

# Carregar a música
pygame.mixer.music.load('music/music_theme.wav')
pygame.mixer.music.set_volume(0.5)  # Defina o volume desejado entre 0.0 e 1.0
musica_tocando = False  # Variável de controle

# Loop principal do jogo
while not in_menu:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not musica_tocando:
        pygame.mixer.music.play(-1)  # -1 para repetir indefinidamente
        musica_tocando = True

    screen.fill('#d1aa9d')

    # Desenhar o nível (tiles e mapa)
    level.run()

    # Atualize e desenhe as nuvens
    clouds.update(level.world_shift)
    clouds.draw(screen)

    if not level.game_over:
        # Desenhar a interface de usuário
        ui.draw(screen)

    pygame.display.update()
    clock.tick(60)

# Encerrar a música quando não for mais necessária
pygame.mixer.music.stop()