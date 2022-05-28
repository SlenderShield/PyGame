from random import choice, randint
from sys import exit

import pygame


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		player_walk1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
		player_walk2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
		self.player_walk = [ player_walk1, player_walk2 ]
		self.player_index = 0
		self.player_jump = pygame.image.load('graphics/player/jump.png')
		self.image = self.player_walk[ self.player_index ]
		self.rect = self.image.get_rect(midbottom = (80, 300))
		self.gravity = 0
		self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
		self.jump_sound.set_volume(0.5)

	def player_input(self):
		keys = pygame.key.get_pressed()
		if keys[ pygame.K_SPACE ] and self.rect.bottom >= 300:
			self.gravity = -20
			self.jump_sound.play()

	def apply_gravity(self):
		self.gravity += 1
		self.rect.y += self.gravity
		if self.rect.bottom >= 300:
			self.rect.bottom = 300

	def animation_state(self):
		if self.rect.bottom < 300:
			self.image = self.player_jump
		else:
			self.player_index += 0.1
			if self.player_index >= len(self.player_walk):
				self.player_index = 0
			self.image = self.player_walk[ int(self.player_index) ]

	def update(self):
		self.player_input()
		self.apply_gravity()
		self.animation_state()


class Obstacle(pygame.sprite.Sprite):
	def __init__(self, type):
		super().__init__()
		if type == 'fly':
			fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
			fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
			self.frames = [ fly_frame_1, fly_frame_2 ]
			y_pos = 210
		else:
			snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
			snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
			self.frames = [ snail_frame_1, snail_frame_2 ]
			y_pos = 300
		self.animation_index = 0
		self.image = self.frames[ self.animation_index ]
		self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

	def animation_state(self):
		self.animation_index += 0.1
		if self.animation_index >= len(self.frames):
			self.animation_index = 0
		self.image = self.frames[ int(self.animation_index) ]

	def update(self):
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100:
			self.kill()


def display_score():
	current_time = int(pygame.time.get_ticks() / 1000) - start_time
	score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
	score_rect = score_surf.get_rect(center = (400, 50))
	screen.blit(score_surf, score_rect)
	return current_time


def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
		return False
	return True


# Initialize and create the screen in pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Initial game point
GAME_ACTIVE = False

# Import the font into the game
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# Scoring
start_time = 0
score = 0

# Add Background Music
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.6)
bg_music.play(loops = -1)  # -1 means infinite loop

# Create a surface and load an image
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Player for Intro
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_scaled = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand_scaled.get_rect(center = (400, 200))

# Introduction Page
game_name = test_font.render('Pixel Runner', False, (64, 64, 64))
game_name_rect = game_name.get_rect(center = (400, 100))
start_game_surf = test_font.render('Press Space to start', False, (64, 64, 64))
start_game_rect = start_game_surf.get_rect(center = (400, 300))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
	# Check if the user wants to quit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.QUIT
			exit()

		if GAME_ACTIVE:
			if event.type == obstacle_timer:
				obstacle_group.add(Obstacle(choice([ 'fly', 'snail', 'snail', 'snail' ])))
		else:
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				GAME_ACTIVE = True
				start_time = int(pygame.time.get_ticks() / 1000)
	if GAME_ACTIVE:

		# Fill the display (screen, position)
		screen.blit(sky_surface, (0, 0))
		screen.blit(ground, (0, 300))

		# Display Score
		score = display_score()

		# Display Player
		player.draw(screen)
		player.update()

		# Display obstacles
		obstacle_group.draw(screen)
		obstacle_group.update()

		# Collisions
		GAME_ACTIVE = collision_sprite()
	else:
		# If the game is not active, display the introduction page
		screen.fill((94, 129, 162))
		screen.blit(player_stand, player_stand_rect)
		screen.blit(game_name, game_name_rect)
		# If score is present, display it
		score_board = test_font.render(f'Score: {score}', False, (64, 64, 64))
		score_board_rect = score_board.get_rect(center = (400, 300))
		if score == 0:
			screen.blit(start_game_surf, start_game_rect)
		else:
			screen.blit(score_board, score_board_rect)
	# Drawing all the elements
	pygame.display.update()

	# Limit the frame rate to 60 FPS(Maximum FPS)
	clock.tick(60)
