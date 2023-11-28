import os
import pygame

width = 800  # Largura Janela
height = 600  # Altura Janela

#Paths
cap_path = 'Treasure Hunters/Captain Clown Nose/Sprites/'

#Sprites
#Cap sprites
cap_idle = []
cap_run = []
cap_with_sword_idle = []
cap_with_sword_run = []
cap_jump = []

#sword sprite
sword_idle = []

#Frames
main_character_frame = 0
cap_idle_frame = 0
sword_idle_frame = 0
cap_jump_frame = 0

main_character_pos_x = 100
main_character_pos_y = 225

main_character_time = 0  # variável para controle do tempo da animação
cap_idle_time = 0
sword_idle_time = 0
cap_jump_time = 0

ultima_tecla = 'right'
sword = False

def load():
    global clock, cap_idle, cap_run, condicao
    clock = pygame.time.Clock()
    condicao = 0

    #Carregamento de animações
    for i in range(1, 6):  # carrega as imagens da animação idle
        img = pygame.image.load(os.path.join(cap_path, 'Captain Clown Nose', 'Captain Clown Nose without Sword', '01-Idle', f'Idle 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        cap_idle.append(img)

    for i in range(1, 7):  # carrega as imagens da animação run
        img = pygame.image.load(os.path.join(cap_path, 'Captain Clown Nose', 'Captain Clown Nose without Sword', '02-Run', f'Run 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        cap_run.append(img)

    for i in range(1, 9):
        img = pygame.image.load(os.path.join(cap_path, 'Captain Clown Nose', 'Sword', '21-Sword Idle', f'Sword Idle 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        sword_idle.append(img)

    for i in range(1,6):
        img = pygame.image.load(os.path.join(cap_path, 'Captain Clown Nose', 'Captain Clown Nose with Sword', '09-Idle Sword', f'Idle Sword 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        cap_with_sword_idle.append(img)

    for i in range(1, 7):
        img = pygame.image.load(os.path.join(cap_path, 'Captain Clown Nose', 'Captain Clown Nose with Sword', '10-Run Sword', f'Run Sword 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        cap_with_sword_run.append(img)

    for i in range(1,4):
        img = pygame.image.load(os.path.join(cap_path, 'Captain Clown Nose', 'Captain Clown Nose with Sword', '11-Jump Sword', f'Jump Sword 0{i}.png'))
        img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
        cap_jump.append(img)
def animacao(valorLado, sinal, dt):
    global main_character_frame, main_character_pos_x, main_character_pos_y, main_character_time

    lado = valorLado

    if sinal == '+':
        if lado == 3:
            main_character_pos_x = main_character_pos_x + (0.1 * dt)  # Direita
            main_character_time += dt
            # Atualiza a animação run a cada 100 milissegundos
            if main_character_time > 100:
                main_character_frame = (main_character_frame + 1) % len(cap_run)
                main_character_time = 0
    elif sinal == '-':
        if lado == 2:
            main_character_pos_x = main_character_pos_x - (0.1 * dt)  # Esquerda
            main_character_time += dt
            # Atualiza a animação run a cada 100 milissegundos
            if main_character_time > 100:
                main_character_frame = (main_character_frame + 1) % len(cap_run)
                main_character_time = 0
        elif lado == 1:
            main_character_pos_y = main_character_pos_y - (0.1 * dt)  # Cima
            main_character_time += dt
            # Atualiza a animação run a cada 100 milissegundos
            if main_character_time > 100:
                main_character_frame = (main_character_frame + 1) % len(cap_run)
                main_character_time = 0
        elif lado == 0:
            main_character_pos_y = main_character_pos_y + (0.1 * dt)  # Baixo
            main_character_time += dt
            # Atualiza a animação run a cada 100 milissegundos
            if main_character_time > 100:
                main_character_frame = (main_character_frame + 1) % len(cap_run)
                main_character_time = 0

# Função para verificar colisão
def check_collision():
    global main_character_pos_x, main_character_pos_y, sword_idle_frame, cap_run, sword

    cap_rect = cap_run[main_character_frame].get_rect(center=(main_character_pos_x, main_character_pos_y))
    sword_rect = sword_idle[sword_idle_frame].get_rect(center=(400, 250))

    if cap_rect.colliderect(sword_rect):
        sword = True

def update(dt):
    global main_character_pos_x, main_character_pos_y, main_character_frame, main_character_time, condicao, cap_run, cap_idle, ultima_tecla, cap_idle_frame, cap_idle_time, sword_idle_time, sword_idle_frame, sword

    cap_idle_time += dt
    sword_idle_time += dt
    # Atualiza a animação idle do captao a cada 100 milissegundos
    if cap_idle_time > 100:
        cap_idle_frame = (cap_idle_frame + 1) % len(cap_idle)
        cap_idle_time = 0

    if sword_idle_time > 100:
        sword_idle_frame = (sword_idle_frame + 1) % len(sword_idle)
        sword_idle_time = 0

    # Detecta se as setinhas foram pressionadas e movimenta o personagem chamando a função
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if ultima_tecla != 'right':
            if not sword:
                for i in range(len(cap_run)):
                    cap_run[i] = pygame.transform.flip(cap_run[i], True, False)
                for i in range(len(cap_idle)):
                    cap_idle[i] = pygame.transform.flip(cap_idle[i], True, False)
            else:
                for i in range(len(cap_with_sword_run)):
                    cap_with_sword_run[i] = pygame.transform.flip(cap_with_sword_run[i], True, False)
                for i in range(len(cap_with_sword_idle)):
                    cap_with_sword_idle[i] = pygame.transform.flip(cap_with_sword_idle[i], True, False)
            ultima_tecla = 'right'
        animacao(3, '+', dt)
    elif keys[pygame.K_LEFT]:
        if ultima_tecla != 'left':
            if not sword:
                for i in range(len(cap_run)):
                    cap_run[i] = pygame.transform.flip(cap_run[i], True, False)
                for i in range(len(cap_idle)):
                    cap_idle[i] = pygame.transform.flip(cap_idle[i], True, False)
            else:
                for i in range(len(cap_with_sword_run)):
                    cap_with_sword_run[i] = pygame.transform.flip(cap_with_sword_run[i], True, False)
                for i in range(len(cap_with_sword_idle)):
                    cap_with_sword_idle[i] = pygame.transform.flip(cap_with_sword_idle[i], True, False)
            ultima_tecla = 'left'
        animacao(2, '-', dt)
    elif keys[pygame.K_UP]:
        animacao(1, '-', dt)
    elif keys[pygame.K_DOWN]:
        animacao(0, '-', dt)

    if any(keys):
        condicao = 1
    else:
        condicao = 0

    # Verifica colisão entre o capitão e a espada
    check_collision()

def draw_screen(screen):
    screen.fill((255, 255, 255))

    if sword == False:
        if condicao == 0:
            # Desenha o personagem usando o índice da animação (Seleção do sprite)
            screen.blit(cap_idle[cap_idle_frame], (main_character_pos_x, main_character_pos_y))
        elif condicao == 1:
            screen.blit(cap_run[main_character_frame], (main_character_pos_x, main_character_pos_y))
        screen.blit(sword_idle[sword_idle_frame], (400, 250))
    elif sword:
        #Desenha o capitao com espada
        if condicao == 0:
            screen.blit(cap_with_sword_idle[cap_idle_frame], (main_character_pos_x, main_character_pos_y))
        elif condicao == 1:
            screen.blit(cap_with_sword_run[main_character_frame], (main_character_pos_x, main_character_pos_y))

def main_loop(screen):
    global clock
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:  # fechamento do prog
                running = False
                break

        # Define FPS máximo
        clock.tick(60)
        # Tempo transcorrido desde a última atualização
        dt = clock.get_time()
        # Atualiza posição dos objetos
        update(dt)
        # Desenha objetos
        draw_screen(screen)
        # Pygame atualiza a visualização da tela
        pygame.display.update()

# Programa principal
pygame.init()
screen = pygame.display.set_mode((width, height))
load()
main_loop(screen)
pygame.quit()
