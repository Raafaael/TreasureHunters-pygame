# cloud.py
from settings import screen_width
import pygame

class Cloud(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.image.load("1.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.starting_position = pos  # Adicione a posição inicial

    def update(self, x_shift):
        self.rect.x += self.speed + x_shift

        # Verifica se a nuvem ultrapassou o final da tela
        if self.rect.right < 0:
            # Retorna a nuvem à posição inicial
            self.rect.x = self.starting_position[0] + screen_width




