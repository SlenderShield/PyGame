from sys import exit

import pygame

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

# Create a surface and load an image
sky_surface = pygame.image.load("graphics/sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()

# Create a surface and load text on it
text_surface = test_font.render("MY Game", False, "Black")

snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
Snail_Pos = 600

while True:
	# Check if the user wants to quit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	# Fill the display (screen, position)
	screen.blit(sky_surface, (0, 0))
	screen.blit(ground, (0, 300))
	screen.blit(text_surface, (300, 50))

	# Make snail move 2 frames per second to left
	Snail_Pos -= 2
	# If snail goes off-screen to the left, reset it to the right
	if Snail_Pos < -100:
		Snail_Pos = 800
	screen.blit(snail_surface, (Snail_Pos, 260))

	# Drawing all the elements
	pygame.display.update()

	# Limit the frame rate to 60 FPS(Maximum FPS)
	clock.tick(60)
