import pygame, time
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player
from enemy import Enemy
from coin import Coin
from tree import Palm
from goal import Goal
from waves import Wave

class Level:
	def __init__(self,level_data,surface, mapa, enemy_file, coins_file, palms_file, goal_file,waves_file):

		# level setup
		self.display_surface = surface
		self.level_data = level_data
		self.setup_level(level_data)
		self.setup_player(level_data)
		self.world_shift = 0
		self.current_x = 0
		self.setup_enemies(enemy_file)
		self.enemy_file = enemy_file
		self.load_coins(coins_file)
		self.coins_file = coins_file
		self.load_palms(palms_file)
		self.palms_file = palms_file
		self.start_time = time.time()
		self.load_goal(goal_file)
		self.goal_file = goal_file
		self.victory_image = pygame.image.load('Final_logo.png')
		self.minutes = 0
		self.seconds = 0
		self.load_waves(waves_file)
		self.waves_file = waves_file


		# ground
		self.player_on_ground = False

		# mapa
		self.mapa = mapa
		self.map_rect = self.mapa.get_rect()
		self.map_rect.x = -10 * tile_size
		self.player_start_pos = (100, 50)  # Defina isso para a posição inicial
		self.game_over = False

		#player
		self.cont_deaths = 0
		self.enemy_killed = 0
		self.R_key_pressed = False
		self.last_restart_time = 0


	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def setup_level(self,layout):
		self.tiles = pygame.sprite.Group()


		for row_index,row in enumerate(layout):
			self.goals = pygame.sprite.Group()
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				if cell == 'X':
					tile = Tile((x,y),tile_size)
					self.tiles.add(tile)
					self.tiles.add(tile)

	def setup_player(self,layout):
		self.player = pygame.sprite.GroupSingle()

		for row_index,row in enumerate(layout):
			self.goals = pygame.sprite.Group()
			for col_index,cell in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size

				if cell == 'P':
					player_sprite = Player((x,y),100)
					self.player.add(player_sprite)

	def load_goal(self, file_path):
		self.goals = pygame.sprite.Group()
		with open(file_path, 'r') as f:
			data = f.readlines()

		for y, row in enumerate(data):
			for x, cell in enumerate(row):
				if cell == 'V':
					goal = Goal((x * tile_size, y * tile_size))
					self.goals.add(goal)

	def load_coins(self, file_path):
		self.coins = pygame.sprite.Group()
		with open(file_path, 'r') as file:
			for y, line in enumerate(file):
				for x, char in enumerate(line):
					if char == 'C':
						coin = Coin(x * tile_size+25, y * tile_size+25, 'C')
						self.coins.add(coin)
					elif char == 'G':
						coin = Coin(x * tile_size+25, y * tile_size+25, 'G')
						self.coins.add(coin)

	def load_palms(self, file_path):
		self.palms = pygame.sprite.Group()
		with open(file_path, 'r') as file:
			for y, line in enumerate(file):
				for x, char in enumerate(line):
					if char == 'L':
						palm = Palm(x * tile_size + 25, y * tile_size + 25, 'L')
						self.palms.add(palm)

	def load_waves(self, file_path):
		self.waves = pygame.sprite.Group()
		with open(file_path, 'r') as file:
			for y, line in enumerate(file):
				for x, char in enumerate(line):
					if char == 'W':
						wave = Wave(x * tile_size+25, y * tile_size+25, 'W')
						self.waves.add(wave)

	def setup_enemies(self, enemy_file):
		self.enemies = pygame.sprite.Group()
		self.collidable_tiles = pygame.sprite.Group()

		with open(enemy_file, 'r') as file:
			for row_index, row in enumerate(file):
				for col_index, cell in enumerate(row.strip()):
					x = col_index * tile_size
					y = row_index * tile_size
					if cell == 'E':
						enemy = Enemy(x, y, 2, 'sprites/Enemies/enemy1/', self)
						self.enemies.add(enemy)
					elif cell == 'A':
						enemy = Enemy(x, y, 3, 'sprites/Enemies/enemy2/', self)
						self.enemies.add(enemy)
					elif cell == 'S':
						enemy = Enemy(x, y, 2, 'sprites/Enemies/enemy3/', self)
						self.enemies.add(enemy)
					elif cell == 'X':
						tile = Tile((x, y), tile_size)
						self.collidable_tiles.add(tile)

	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			self.world_shift = 0
			player.speed = 8

	def horizontal_movement_collision(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def vertical_movement_collision(self):
		player = self.player.sprite
		player.apply_gravity()

		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0:
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.on_ground = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True

		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def reset_level(self):
		self.player.sprite.rect.x, self.player.sprite.rect.y = self.player_start_pos
		self.world_shift = 0
		self.map_rect.topleft = (0, 0)

		# Reinicia as moedas
		self.coins.empty()  # Esvazia o grupo de sprites das moedas
		self.load_coins(self.coins_file)

		# Reinicia a vida do jogador
		self.player.sprite.health = 100

		# Reinicia o contador de moedas do jogador
		self.player.sprite.coins = 0

		# Reinicia os tiles e os inimigos
		self.enemies.empty()  # Esvazia o grupo de sprites dos inimigos
		self.setup_enemies(self.enemy_file)

		# Reinicia os tiles
		self.setup_level(self.level_data)

		# Redesenha as Palmeiras
		self.load_palms(self.palms_file)

		# Redesenha as Ondas
		self.load_waves(self.waves_file)

		# Redesenha o mapa
		self.map_rect.x = -10 * tile_size

		# Reinicia os objetios
		self.goals.empty()
		self.load_goal(self.goal_file)

		#reinicia as kills
		self.enemy_killed = 0

		self.start_time = time.time()

		if self.R_key_pressed:
			#Reinicia os contadores
			self.cont_deaths = 0
			self.R_key_pressed = False

	def check_restart(self):
		keys = pygame.key.get_pressed()
		current_time = pygame.time.get_ticks()  # Obtém o tempo atual em milissegundos

		if keys[pygame.K_r] and current_time - self.last_restart_time >= 500:
			self.last_restart_time = current_time  # Atualiza o tempo do último reinício
			self.R_key_pressed = True
			self.game_over = False
			self.reset_level()

	def check_death(self):
		if self.player.sprite.rect.y > screen_height or self.player.sprite.health <= 0:
			self.cont_deaths+=1
			self.reset_level()

	def check_victory(self, surface):
		for goal in self.goals:
			if self.player.sprite.rect.colliderect(goal.rect):
				# Desenhar a imagem de vitória
				self.game_over = True
				self.display_surface.blit(self.victory_image, (100, 100))
				minutes = self.minutes
				seconds = self.seconds

				# Cria o texto do timer
				font = pygame.font.Font(None, 28)  # Substitua None pela fonte desejada
				pontos = font.render(f"{self.player.sprite.coins}", True, (255, 255, 255))
				mortes = font.render(f'{self.cont_deaths}', True, (255, 255, 255))
				tempo = font.render(f'{minutes}:{seconds}', True, (255, 255, 255))
				inimigos_mortos = font.render(f'{self.enemy_killed}', True, (255, 255, 255))

				# Desenha o texto do timer na tela
				surface.blit(pontos, (350, 400))
				surface.blit(mortes, (350, 450))
				surface.blit(tempo, (350, 500))
				surface.blit(inimigos_mortos, (370, 545))

	def check_enemies_colision(self):
		for enemy in self.enemies:
			if self.player.sprite.rect.colliderect(enemy.rect):
				if self.player.sprite.attack_animation_playing:
					enemy_death_sound = pygame.mixer.Sound('music/enemy_death.wav')
					enemy_death_sound.set_volume(0.3)
					pygame.mixer.Sound.play(enemy_death_sound)
					enemy.kill()
					self.enemy_killed +=1
				else:
					self.player.sprite.get_damage(enemy)

	def draw_timer(self, surface):
		# Calcula o tempo decorrido
		elapsed_time = time.time() - self.start_time
		minutes = int(elapsed_time // 60)
		seconds = int(elapsed_time % 60)

		# Cria o texto do timer
		font = pygame.font.Font(None, 30)  # Substitua None pela fonte desejada
		self.minutes = minutes
		self.seconds = seconds
		timer_text = font.render(f"{minutes}:{seconds:02}", True, (0, 0, 0))

		# Desenha o texto do timer na tela
		surface.blit(timer_text, (1100, 20))

	def run(self):
		# level tiles
		self.tiles.update(self.world_shift)
		self.tiles.draw(self.display_surface)

		# enemies
		self.enemies.update()
		self.check_enemies_colision()

		#camera
		self.scroll_x()

		# mapa
		self.map_rect.x += self.world_shift
		self.display_surface.blit(self.mapa, self.map_rect)

		# Atualizar e desenhar os inimigos
		for enemy in self.enemies:
			enemy.rect.x += self.world_shift
		self.enemies.draw(self.display_surface)

		# Atualizar a posição dos collidable_tiles
		for tile in self.collidable_tiles:
			tile.rect.x += self.world_shift

		for goal in self.goals:
			goal.rect.x += self.world_shift

		self.goals.draw(self.display_surface)

		self.check_victory(self.display_surface)

		# player
		self.player.update()
		self.horizontal_movement_collision()
		self.get_player_on_ground()
		self.vertical_movement_collision()
		self.player.draw(self.display_surface)
		self.check_death()
		self.check_restart()

		# Atualizar e desenhar as palmeiras
		for palm in self.palms:
			palm.rect.x += self.world_shift
			palm.animate()
		self.palms.draw(self.display_surface)

		# Atualizar e desenhar as Ondas
		for wave in self.waves:
			wave.rect.x += self.world_shift
			wave.animate()
		self.waves.draw(self.display_surface)

		# Atualizar e desenhar as moedas
		for coin in self.coins:
			coin.rect.x += self.world_shift
			coin.animate()
			if self.player.sprite.rect.colliderect(coin.rect):
				coin.kill()  # Remove the coin
				if coin.type == 'C':
					self.player.sprite.collect_coin(1)  # Adiciona 1 ao contador de moedas
				elif coin.type == 'G':
					self.player.sprite.collect_coin(3)  # Adiciona 3 ao contador de moedas

		self.coins.draw(self.display_surface)

		# Atulizar o timer e desenhar
		if not self.game_over:
			self.draw_timer(self.display_surface)
