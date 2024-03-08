import pygame

class Goal(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        # Carregar a imagem do baú
        self.image = pygame.image.load('sprites/chest/1.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*2, self.image.get_height()*2))

        # Definir o rect do sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = position