from sys import exit

import pygame

docstring = """"""

# Initialize and create the screen in pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("MY Game")
clock = pygame.time.Clock()

# Import the font into the game
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# Create a surface and fill it with a color
# test_surface = pygame.Surface((100, 200))
# test_surface.fill('#FFAABB')

game_active = True
# Create a surface and load an image
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()

# Create a surface and load text on it
score_surface = test_font.render("MY Game", False, (64, 64, 64))
score_rect = score_surface.get_rect(center = (400, 50))

# Create a surface for snail
snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom = (600, 300))

# Create a player surface and player rect
player_surface = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))

# Create Gravity
player_gravity = 0

while True:
	# Check if the user wants to quit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if game_active:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
					player_gravity = -20
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and player_rect.bottom == 300:
					player_gravity = -20
		else:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_active = True
					player_gravity = 0
					snail_rect.left = 600

	if game_active:
		# Fill the display (screen, position)
		screen.blit(sky_surface, (0, 0))
		screen.blit(ground, (0, 300))
		pygame.draw.rect(screen, '#c0e8ec', score_rect)  # Draw a rectangle( surface, color, rect, width)
		pygame.draw.rect(screen, '#c0e8ec', score_rect, 6)  # Draw a rectangle( surface, color, rect, width)
		screen.blit(score_surface, score_rect)

		# Make snail move 2 frames per second to left
		snail_rect.right -= 2
		# If snail goes off-screen to the left, reset it to the right
		if snail_rect.right <= 0:
			snail_rect.left = 800
		screen.blit(snail_surface, snail_rect)

		# Make player move 2 frames per second to right
		player_gravity += 1
		player_rect.bottom += player_gravity
		if player_rect.bottom >= 300:
			player_rect.bottom = 300
			player_gravity = 0
		# player_rect.left += 2
		screen.blit(player_surface, player_rect)

		# if player_rect.colliderect(snail_rect):
		# 	print("Collision!")

		# Get mouse position
		# mouse_pos = pygame.mouse.get_pos()
		# if player_rect.collidepoint(mouse_pos):
		# 	print("Collision!")

		# Keyboard input from the user.
		# keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE]:
		# 	print("Space!")

		# Collision detection
		if snail_rect.colliderect(player_rect):
			game_active = False
	else:
		screen.fill('#FFAABB')
	# Drawing all the elements
	pygame.display.update()

	# Limit the frame rate to 60 FPS(Maximum FPS)
	clock.tick(60)
