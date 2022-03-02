import pygame
import sys
import random
import time

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 30

#Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#Elements
player_size = 50
player_pos = [WIDTH/2 , HEIGHT - 2*player_size]

enemy_size = 50
falling_speed = 10
random_pos = random.randint(0, WIDTH - enemy_size)
enemy_pos = [random_pos, 0]
max_enemy = 7
enemy_list = []
screen = pygame.display.set_mode((WIDTH, HEIGHT))
score = 0
prop = 0.4
clock = pygame.time.Clock()

game_over  = False

myFont = pygame.font.SysFont("monospcae", 35)

def set_level(score, max_enemy):
	if(score<10):
		falling_speed = 5
	elif(score < 30):
		falling_speed = 10
	elif(score < 60):
		falling_speed = 15
	elif(score < 100):
		falling_speed = 20
	else:
		falling_speed = int(score*prop)
		max_enemy = 15
	return falling_speed

def drop_enemies(enemy_list):
	delay = random.random()
	if (len(enemy_list)<max_enemy and delay < 0.2):
		x_pos = random.randint(0, WIDTH - enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])

def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):

		if enemy_pos[1] >=0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += falling_speed
		else:
			enemy_list.pop(idx)
			score += 1

	return score


def collision_check(enemy_list):
	for enemy_pos in enemy_list:
		if(detect_collisions(player_pos, enemy_pos)):
			return True
	return False


def detect_collisions(player_pos, enemy_pos):
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if(abs(p_x - e_x)<(player_size-5) and abs(p_y - e_y)<(player_size-5)):
		return True
  
	return False
		
	
while not game_over:

	for event in pygame.event.get():
		
		if event.type == pygame.QUIT:
			sys.exit()
		#Positiosns of Enemy
		if event.type == pygame.KEYDOWN:
			x = player_pos[0]
			y = player_pos[1]
			if event.key == pygame.K_LEFT:
				x -= player_size
			elif event.key == pygame.K_RIGHT:
				x += player_size

			player_pos = [x, y]

		

	screen.fill(BLACK)

	drop_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	falling_speed = set_level(score, max_enemy)
	print('SP - '+str(falling_speed))
	text = "Score: " + str(score)
	label = myFont.render(text, 1, YELLOW)
	screen.blit(label, (WIDTH-200, HEIGHT-40))
	pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))
	draw_enemies(enemy_list)
	if collision_check(enemy_list):
		screen.fill(BLACK)
		myFont2 = pygame.font.SysFont("monospcae", 50)
		myFont3 = pygame.font.SysFont("comicsansms", 40)
		text = "SCORE: " + str(score)
		thank = "Thanks for Playing :)  ~Gourav Kumar Shaw"
		label = myFont.render(text, 1, YELLOW)
		label2 = myFont3.render(thank, 1, YELLOW)
		screen.blit(label, (WIDTH/2 - 60, HEIGHT/2))
		screen.blit(label2, (100, HEIGHT-40))
		pygame.display.update()
		time.sleep(2)
		game_over=True

		break
	
	
	clock.tick(FPS)
	pygame.display.update()
