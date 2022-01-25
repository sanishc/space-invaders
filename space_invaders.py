import pygame
import math
import random
from pygame import mixer

pygame.init()

# window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('images/window_icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('images/space_bg.jpg')

# sound
mixer.music.load('audios/mazhamadhalam_bgm.wav')
mixer.music.play(-1)

# player
player_img = pygame.image.load('images/spaceship.png')
player_x = 370
player_y = 480
player_x_change = 0
player_y_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_count = 10
for i in range(enemy_count):
    enemy_img.append(pygame.image.load('images/enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

# Bullet
bullet_img = pygame.image.load('images/bullet.png')
bullet_x = 0
bullet_y = 0
bullet_x_change = 0
bullet_y_change = 1.3
bullet_state = 'ready'

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_x = 10
score_y = 10

# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_status = False


def show_score():
    game_score = font.render("Score: %s" % score, True, (255, 255, 255))
    screen.blit(game_score, (score_x, score_y))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x, y))


def is_bullet_collision(en_x, en_y, bul_x, bul_y):
    distance = math.sqrt(math.pow(en_x - bul_x, 2) + math.pow(en_y - bul_y, 2))
    if distance < 27:
        return True
    else:
        return False


def is_player_collision(en_x, en_y, pl_x, pl_y):
    distance = math.sqrt(math.pow(en_x - pl_x, 2) + math.pow(en_y - pl_y, 2))
    if distance < 27:
        return True
    else:
        return False


def game_over():
    global game_over_status
    if not game_over_status:
        game_over_sound = mixer.Sound('audios/ne_theerneda.wav')
        game_over_sound.play()
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (230, 250))
    game_over_status = True


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change += -1
            if event.key == pygame.K_RIGHT:
                player_x_change += 1
            if event.key == pygame.K_UP:
                player_y_change += -1
            if event.key == pygame.K_DOWN:
                player_y_change += 1
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                bullet_sound = mixer.Sound('audios/shoot.wav')
                bullet_sound.play()
                bullet_x = player_x
                bullet_y = player_y
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_y_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    player_y += player_y_change
    if player_y <= 0:
        player_y = 0
    elif player_y >= 536:
        player_y = 536

    player(player_x, player_y)

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    for i in range(enemy_count):
        player_collision = is_player_collision(enemy_x[i], enemy_y[i], player_x, player_y)
        if enemy_y[i] > 500 or player_collision:
            for j in range(enemy_count):
                enemy_y[j] = 700
            game_over()
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        bullet_collision = is_bullet_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if bullet_collision:
            collision_sound = mixer.Sound('audios/hit.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = 'ready'
            score += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(0, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    show_score()
    pygame.display.update()
