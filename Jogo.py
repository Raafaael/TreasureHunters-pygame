import os
import pygame
from player import Player

width = 800  # Largura Janela
height = 600  # Altura Janela

#main character
main_character_pos_x = 100
main_character_pos_y = 225
health = 100

#paths
cap_path = 'sprites/Treasure Hunters/Captain Clown Nose/Sprites/'
enemy_path = 'sprites/Treasure Hunters/The Crusty Crew/Sprites/Fierce Tooth'

#sword
sword_idle = []
sword_idle_time = 0
sword_idle_frame = 0

#enemy
enemy_idle = []
enemy_run = []
enemy_idle_time = 0
enemy_frame = 0
enemy_pos_x = 400
enemy_pos_y = 225
enemy_time = 0    #parâmetro para controle do inimigo

def load():
    global clock, player, health, sword_rect
    clock = pygame.time.Clock()
    player = Player((main_character_pos_x, main_character_pos_y), health)

    for i in range(1, 9):
        img = pygame.image.load(os.path.join(cap_path, 'Captain Clown Nose', 'Sword', '21-Sword Idle', f'Sword Idle 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        sword_idle.append(img)

    sword_rect = pygame.Rect(300,250,20,50)

    carrega_inimigo()

def carrega_inimigo():
    for i in range(1, 9):   # carrega as imagens da animação da idle do inimigo
        img = pygame.image.load(os.path.join(enemy_path, '01-Idle', f'Idle 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        enemy_idle.append(img)
    for i in range(1, 6):   # carrega as imagens da animação de run do inimigo
        img = pygame.image.load(os.path.join(enemy_path, '02-Run', f'Run 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        enemy_run.append(img)

def update(dt):
    global main_character_pos_x, main_character_pos_y, player_jump_speed, sword_idle_time, sword_idle_frame,  enemy_frame, enemy_idle,enemy_idle_time
    main_character_pos_x += player.direction.x * player.speed
    main_character_pos_y += player.direction.y * player.speed

    # Atualiza a posição do retângulo do jogador
    player.collision_rect.topleft = (main_character_pos_x, main_character_pos_y) #Atualiza a posição do retângulo do jogador

    sword_idle_time += dt
    enemy_idle_time += dt

    if sword_idle_time > 100:
        sword_idle_frame = (sword_idle_frame + 1) % len(sword_idle)
        sword_idle_time = 0

    if enemy_idle_time > 100:
        enemy_frame = (enemy_frame + 1) % len(enemy_idle)
        enemy_idle_time = 0

    if player.collision_rect.colliderect(sword_rect):
        player.with_sword = True

def draw_screen(screen):
    screen.fill((255, 255, 255))
    screen.blit(player.image, (main_character_pos_x, main_character_pos_y))
    if player.with_sword == False:
        screen.blit(sword_idle[sword_idle_frame], (300, 270))
    #desenha o inimigo
    screen.blit(enemy_idle[enemy_frame], (enemy_pos_x,enemy_pos_y))

def main_loop(screen):
    global clock

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                break

        clock.tick(60)
        dt = clock.get_time()
        update(dt)
        player.update()
        draw_screen(screen)

        pygame.display.update()

# Programa principal
pygame.init()
screen = pygame.display.set_mode((width, height))
load()
main_loop(screen)
pygame.quit()
