import pygame
from settings import import_folder
from math import sin

class Player:
    def __init__(self, pos, health):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.frame_speed = 1
        self.animation_speed = 0.15
        self.image = self.animations['idle_without_sword'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (70, self.rect.height))
        self.attack_collision_rect = pygame.Rect(0, 0, 50, 50)

        # player status
        self.status = 'idle_without_sword'
        self.facing_right = True
        self.on_ground = False
        self.on_left = False
        self.on_right = False
        self.attack_animation_playing = False
        self.with_sword = False

        # health management
        self.health = health
        self.invincible = False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # attack cooldown
        self.attack_cooldown = 300
        self.last_attack_time = 0

    def import_character_assets(self): #Carrega os sprites do personagem
        character_path = 'sprites/playerSprite/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': [], 'attack': [], 'idle_without_sword': [], 'run_without_sword': [], 'jump_without_sword': [], 'fall_without_sword': [], 'attack_without_sword': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self): #Anima o personagem
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = pygame.transform.scale(image, (int(image.get_width() * 2), int(image.get_height() * 2)))
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = pygame.transform.scale(flipped_image, (int(image.get_width() * 2), int(flipped_image.get_height() * 2)))
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

    def attack(self): #Verifica se o personagem está atacando
        current_time = pygame.time.get_ticks()

        if current_time - self.last_attack_time >= self.attack_cooldown and self.with_sword:
            if self.status != 'attack':
                self.status = 'attack'
                self.frame_index = 0
                self.attack_animation_playing = True
                self.attack_collision_rect.midbottom = self.rect.midbottom
                self.last_attack_time = current_time

    def animate_attack(self):  # Anima o ataque
        attack_animation = self.animations['attack']

        self.frame_index += self.animation_speed
        if self.frame_index >= len(attack_animation):
            self.frame_index = 0
            self.attack_animation_playing = False  # Define como False após a animação ser concluída

        image = attack_animation[int(self.frame_index)]

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        scaled_image = pygame.transform.scale(image, (int(image.get_width() * 2), int(image.get_height() * 2)))

        self.image = scaled_image

        if self.facing_right:
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            self.rect.bottomright = self.collision_rect.bottomright

    def get_input(self): #Detecta qual tecla foi pressionada
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] and self.on_ground:
            self.jump()

        if keys[pygame.K_SPACE]:
            self.attack()

    def get_status(self): #Pega os status atual do personagem
        if self.direction.y < 0:
            if self.with_sword:
                self.status = 'jump'
            else:
                self.status = 'jump_without_sword'
        elif self.direction.y > 1:
            if self.with_sword:
                self.status = 'fall'
            else:
                self.status = 'fall_without_sword'
        else:
            if self.direction.x != 0:
                if self.with_sword:
                    self.status = 'run'
                else:
                    self.status = 'run_without_sword'
            else:
                if self.with_sword:
                    self.status = 'idle'
                else:
                    self.status = 'idle_without_sword'

    def jump(self):
        self.direction.y = self.jump_speed

    def get_damage(self):
        if not self.invincible:
            self.health(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()

    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.get_input()
        self.get_status()

        if self.attack_animation_playing:
            self.animate_attack()
            if self.frame_index == 0:
                self.status = 'idle'
                self.attack_animation_playing = False
        else:
            self.animate()

        self.invincibility_timer()
        self.wave_value()