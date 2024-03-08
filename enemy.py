import pygame
from support import import_folder

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed, enemy_path, level):
        super().__init__()

        # Carrega as imagens do inimigo
        self.enemy_path = enemy_path
        self.import_enemy_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # Define a posição inicial
        self.rect.x = pos_x
        self.rect.y = pos_y+20

        # Define a velocidade
        self.speed = speed

        # Store the Level object
        self.level = level

    def import_enemy_assets(self):
        self.animations = {'run': []}

        for animation in self.animations.keys():
            full_path = self.enemy_path + animation
            animation_images = import_folder(full_path)

            # Aplica a transformação de escala a todas as imagens
            self.animations[animation] = [pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2)) for img in animation_images]

        # Define a imagem inicial do inimigo
        self.image = self.animations['run'][0]
        self.rect = self.image.get_rect()

    def animate(self):
        animation = self.animations['run']

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Obtém a imagem da animação atual
        image = animation[int(self.frame_index)]

        # Se o inimigo está se movendo para a esquerda, vira a imagem
        if self.speed < 0:
            image = pygame.transform.flip(image, True, False)

        self.image = image

    def update(self):
        # Atualiza a posição do inimigo
        self.rect.x -= self.speed
        self.animate()

        # Verifica a colisão com 'X'
        for sprite in self.level.collidable_tiles.sprites():
            if sprite.rect.colliderect(self.rect):
                self.speed = -self.speed  # Inverte a direção do inimigo