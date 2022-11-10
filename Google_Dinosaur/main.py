import pygame
import random
import time
import math
import sys
import os

# ----------------------------------------------------------------------------------------

class Cloud(pygame.sprite.Sprite):
	def __init__(self, img, posx, posy):
		super().__init__()

		self.image = pygame.image.load(img).convert_alpha()
		self.rect = self.image.get_rect(center=(posx, posy))

		self.move_speed = RUNNING_SPEED/4
		self.direction = -1
		self.pos = pygame.math.Vector2(self.rect.center)

	def movement(self, dt):
		self.pos.x += self.direction * self.move_speed * dt
		self.rect.centerx = round(self.pos.x)
		if self.rect.centerx <= -random.randrange(23, WIDTH):
			self.rect.centerx = random.randrange(WIDTH + 23, WIDTH*2, 46)
			self.rect.centery = random.randrange(13, HEIGHT//2 - 13, 13)
			self.pos = pygame.math.Vector2(self.rect.center)

	def update(self, dt):
		self.movement(dt)

# ----------------------------------------------------------------------------------------

class Terrain(pygame.sprite.Sprite):
	def __init__(self, img, posx, posy):
		super().__init__()

		self.image = pygame.image.load(img).convert_alpha()
		self.rect = self.image.get_rect(center=(posx, posy))

		self.move_speed = RUNNING_SPEED
		self.direction = -1
		self.pos = pygame.math.Vector2(self.rect.center)

	def movement(self, dt):
		self.pos.x += self.direction * self.move_speed * dt
		self.rect.centerx = round(self.pos.x)
		if self.rect.centerx <= -300:
			self.rect.centerx = 900
			self.pos = pygame.math.Vector2(self.rect.center)

	def update(self, dt):
		self.movement(dt)

# ----------------------------------------------------------------------------------------

class TRex(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()

		self.frames_1 = [pygame.image.load(os.path.join('assets', 'running_sprite_1.png')).convert_alpha(),
						 pygame.image.load(os.path.join('assets', 'running_sprite_2.png')).convert_alpha()]

		self.frames_2 = [pygame.image.load(os.path.join('assets', 'squats_1.png')).convert_alpha(),
						 pygame.image.load(os.path.join('assets', 'squats_2.png')).convert_alpha()]
		self.frames_1_index = 0
		self.frames_2_index = 0

		self.image = pygame.image.load(os.path.join('assets', 'rest_sprite.png')).convert_alpha()
		self.rect = self.image.get_rect(center=(44, HEIGHT - 47))

		self.squat = False
		self.jumping = False

		self.animation_speed = 8

		self.y_gravity = 650
		self.jump_height = 320
		self.y_velocity = self.jump_height

		self.pos = pygame.math.Vector2(self.rect.center)

	def animation(self, dt):
		global score

		score += round(RUNNING_SPEED * dt)
		if not self.jumping and not self.squat:
			self.rect.centery = HEIGHT - 47
			self.frames_1_index += self.animation_speed * dt
			if self.frames_1_index >= len(self.frames_1):
				self.frames_1_index = 0
			self.image = self.frames_1[int(self.frames_1_index)]
		elif self.squat:
			self.rect.centery = HEIGHT - 30
			self.frames_2_index += self.animation_speed * dt
			if self.frames_2_index >= len(self.frames_2):
				self.frames_2_index = 0
			self.image = self.frames_2[int(self.frames_2_index)]

	def jump(self, dt):
		if self.jumping:
			self.image = pygame.image.load(os.path.join('assets', 'rest_sprite.png')).convert_alpha()
			self.pos.y -= self.y_velocity * dt
			self.rect.centery = round(self.pos.y)
			self.y_velocity -= round(self.y_gravity * dt)
			if self.rect.centery >= HEIGHT - 47:
				self.jumping = not self.jumping
				self.y_velocity = self.jump_height
				self.pos = pygame.math.Vector2(self.rect.center)

	def controls(self):
		key_pressed = pygame.key.get_pressed()
		if key_pressed[pygame.K_SPACE] and not self.jumping:
			self.jumping = not self.jumping
		elif key_pressed[pygame.K_w] and not self.jumping:
			self.jumping = not self.jumping

		if key_pressed[pygame.K_s] and not self.squat:
			self.squat = not self.squat
		if not key_pressed[pygame.K_s] and self.squat:
			self.squat = not self.squat

	def end_game(self):
		global running
		for sprite in group_2:
			if self.rect.colliderect(sprite.rect):
				running = not running

	def update(self, dt):
		self.controls()
		self.end_game()
		self.animation(dt)
		self.jump(dt)

# ----------------------------------------------------------------------------------------

class Cactus(pygame.sprite.Sprite):
	def __init__(self, img, posx):
		super().__init__()

		self.image = pygame.image.load(img).convert_alpha()
		self.rect = self.image.get_rect(center=(posx, HEIGHT - 45))

		self.move_speed = RUNNING_SPEED
		self.direction = -1
		self.pos = pygame.math.Vector2(self.rect.center)

	def movement(self, dt):
		self.pos.x += self.direction * self.move_speed * dt
		self.rect.centerx = round(self.pos.x)
		if self.rect.centerx <= -random.randrange(25, WIDTH):
			self.rect.centerx = random.randrange(WIDTH + 12, WIDTH*2)
			self.pos = pygame.math.Vector2(self.rect.center)
			self.image = pygame.image.load(random.choice(PATH_CACTI)).convert_alpha()

	def update(self, dt):
		self.movement(dt)

# ----------------------------------------------------------------------------------------

pygame.init()

TITLE = 'T REX RUN'
WIDTH, HEIGHT = 457, 257
FRAMERATE = 600
RUNNING_SPEED = 240

FONT = pygame.font.Font(os.path.join('font', 'minecraft.ttf'), 16)

PATH_CACTI = (os.path.join('assets', 'cactus_1.png'),
			  os.path.join('assets', 'cactus_2.png'),
			  os.path.join('assets', 'cactus_3.png'),
			  os.path.join('assets', 'cactus_4.png'),)

# ----------------------------------------------------------------------------------------

pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

previous_time = time.time()
running = True
score = 0

group_1 = pygame.sprite.Group()
group_2 = pygame.sprite.Group()

for i in range(6):
	group_1.add(Cloud(os.path.join('assets', 'cloud.png'), random.randrange(23, WIDTH - 23, 46), random.randrange(13, HEIGHT//2 - 13, 13)))

group_1.add(Terrain(os.path.join('assets', 'terrain_1.png'), 300, HEIGHT - 28), Terrain(os.path.join('assets', 'terrain_2.png'), 900, HEIGHT - 28))
group_1.add(TRex())
group_2.add(Cactus(random.choice(PATH_CACTI), random.randrange(WIDTH + 12, WIDTH*2)))

# ----------------------------------------------------------------------------------------

def main():
	global running, previous_time, score
	while running:
		dt = time.time() - previous_time
		previous_time = time.time()

		screen.fill((255, 255, 255))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = not running

		group_1.update(dt)
		group_2.update(dt)

		group_1.draw(screen)
		group_2.draw(screen)

		surf_score = FONT.render(str(score), True, (32.5, 32.5, 32.5))
		rect_score = surf_score.get_rect(center=(WIDTH/2, 16))

		screen.blit(surf_score, rect_score)

		pygame.display.update()
		clock.tick(FRAMERATE)

	return 0

# ----------------------------------------------------------------------------------------

if __name__ == '__main__':
	main()
	pygame.quit()
	sys.exit()
