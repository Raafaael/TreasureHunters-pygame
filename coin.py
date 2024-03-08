import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.images = []
        self.current_image = 0
        self.animation_time = 0.1  # Ajuste este valor para alterar a velocidade da animação
        self.last_update = pygame.time.get_ticks()

        # Carregar os sprites
        if type == 'G':
            for i in range(1, 4):
                self.images.append(pygame.image.load(f'sprites/coins/gold/{i}.png'))
        else:
            for i in range(1, 4):
                self.images.append(pygame.image.load(f'sprites/coins/silver/{i}.png'))

        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(topleft=(x, y))

    def animate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > self.animation_time * 1000:
            self.last_update = time_now
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]