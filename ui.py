import pygame

class UI:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.Font(None, 32)
        self.life_bar_fill = pygame.image.load('sprites/ui/lifebar/color/1.png')
        self.coin_color = (0, 0, 0)

    def draw_life(self, surface):
        multiplicador = 1.5

        life_bar_start = pygame.image.load('sprites/ui/lifebar/bar/1.png')
        life_bar_start = pygame.transform.scale(life_bar_start, (life_bar_start.get_width()*multiplicador, life_bar_start.get_height()*multiplicador))
        life_bar_middle = pygame.image.load('sprites/ui/lifebar/bar/2.png')
        life_bar_middle = pygame.transform.scale(life_bar_middle, (life_bar_middle.get_width()*multiplicador, life_bar_middle.get_height()*multiplicador))
        life_bar_end = pygame.image.load('sprites/ui/lifebar/bar/3.png')
        life_bar_end = pygame.transform.scale(life_bar_end, (life_bar_end.get_width()*multiplicador, life_bar_end.get_height()*multiplicador))

        # Desenhar a parte inicial da barra de vida
        surface.blit(life_bar_start, (20, 20))

        # Desenhar a parte do meio da barra de vida
        middle_width = life_bar_middle.get_width() + 20  # Aumenta a largura da parte do meio em 20 pixels
        middle_scaled = pygame.transform.scale(life_bar_middle, (middle_width*1.6, life_bar_middle.get_height()))
        surface.blit(middle_scaled, (20 + life_bar_start.get_width(), 20))

        # Desenhar a parte final da barra de vida
        surface.blit(life_bar_end, (20 + life_bar_start.get_width() + middle_width+27, 20))

        # Calcular a largura do preenchimento da barra de vida
        total_bar_width = life_bar_start.get_width() + middle_width + life_bar_end.get_width()
        fill_width = (self.player.health / 100) * total_bar_width

        # Desenhar a vida do jogador
        fill_height = int(life_bar_middle.get_height() * 0.1)
        fill_scaled = pygame.transform.scale(self.life_bar_fill, (int(fill_width), fill_height))
        surface.blit(fill_scaled, (20 + life_bar_start.get_width()-24, 19 + (life_bar_middle.get_height() - fill_height) // 2))

    def draw_coins(self, surface):
        coin_image = pygame.image.load('sprites/ui/coin/1.png')
        coin_image = pygame.transform.scale(coin_image, (coin_image.get_width() * 2, coin_image.get_height() * 2))
        coins_text = self.font.render(f"{self.player.coins}", True, self.coin_color)
        surface.blit(coin_image, (15, 55))  # Ajuste estes valores para alterar a posição da imagem da moeda
        surface.blit(coins_text, (15 + coin_image.get_width(), 62))

    def draw(self, surface):
        self.draw_life(surface)
        self.draw_coins(surface)