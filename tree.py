import pygame

class Palm(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        self.images = []
        self.current_image = 0
        self.animation_time = 0.1  # Ajuste este valor para alterar a velocidade da animação
        self.last_update = pygame.time.get_ticks()

        # Carregar os sprites
        if type == 'L':
            for i in range(1, 4):
                original_image = pygame.image.load(f'sprites/palm_large/large_{i}.png')
                scaled_image = pygame.transform.scale(original_image, (64, 128))  # Ajuste aqui para a largura e altura desejadas
                self.images.append(scaled_image)

        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(topleft=(x, y))

    def animate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > self.animation_time * 1000:
            self.last_update = time_now
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]