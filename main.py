import random
import pygame as pg
import time
import math

# initializing pygame
pg.init()

# creating screen
width = 900
height = 600
screen = pg.display.set_mode((width, height))

# player
BG = pg.transform.scale(pg.image.load("background.png"), (width, height))
player_image = pg.image.load("spacecraft.png")
player_x = 450
player_y = 520
player_x_change = 0
run = True
bullet_image = pg.image.load("bullet.png")
bullet_X = 0
bullet_Y = 610
bullet_Xchange = 0
bullet_Ychange = 2
bullet_state = "rest"
bullet2_X = -20
bullet2_Y = -20
bullet2_Xchange = 0
bullet2_Ychange = 2
bullet2_state = "rest"
enemy_image = pg.image.load("enemies.png")
t = time.time() + 2
aliens_x = [80, 160, 240, 320, 400, 480, 560]
aliens_y = [50, 100, 150, 200, 250]
aliens = []
for x in aliens_x:
    for y in aliens_y:
        new_alien = [x, y]
        aliens.append(new_alien)

increment = 1

# Score
score_val = 0
scoreX = 5
scoreY = 5
font = pg.font.Font('freesansbold.ttf', 20)

# Game Over
game_over_font = pg.font.Font('freesansbold.ttf', 64)
# you win font
you_win_font = pg.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Points: " + str(score_val),
                        True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER!",
                                           True, (255, 255, 255))
    screen.blit(game_over_text, (190, 250))


def you_win():
    you_win_text = you_win_font.render("You Won!",
                                           True, (255, 255, 255))
    screen.blit(you_win_text, (190, 250))


def background():
    screen.blit(BG, (0, 0))


def player(x, y):
    screen.blit(player_image, (x, y))


def bullet(x, y):
    screen.blit(bullet_image, (x, y))


def bullet2(x, y):
    screen.blit(bullet_image, (x, y))

def alien(x, y):
    screen.blit(enemy_image, (x, y))


# Collision Concept
def isCollision(x1, x2, y1, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) +
                         (math.pow(y1 - y2, 2)))
    if distance <= 18:
        return True
    else:
        return False


while run:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT and player_x > 50:
                player_x_change = -1
            elif event.key == pg.K_RIGHT and player_x < 850:
                player_x_change = 1

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                player_x_change = 0

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            # Fixing the change of direction of bullet
            if bullet_state is "rest":
                bullet_X = player_x + 16
                bullet_Y = player_y
                bullet_state = 'fire'

    # bullet movement
    if bullet_Y <= 0:
        bullet_Y = 610
        bullet_state = "rest"
    if bullet_state is "fire":
        bullet_Y -= bullet_Ychange

    # alien movement and alien player bullet collision
    for al in aliens:
        al[0] += increment
    for al in aliens:
        if al[0] < 30 or al[0] > 870:
            increment = increment * -1
        collision = isCollision(bullet_X, al[0],
                                bullet_Y, al[1])
        if collision:
            score_val += 1
            bullet_Y = 610
            bullet_state = "rest"
            aliens.remove(al)

    # bullet2(enemy) movement and collision with player
    if time.time() > t:
        t = time.time() + 0.05
        if bullet2_state is "rest":
            al = random.choice(aliens)
            bullet2_Y = al[1]
            bullet2_X = al[0]
            bullet2_state = 'fire'
    if bullet2_Y >= 600:
        bullet2_Y = -20
        bullet2_state = "rest"
    if bullet2_state is "fire":
        bullet2_Y += bullet2_Ychange

    collision = isCollision(bullet2_X, player_x,
                            bullet2_Y, player_y)
    if collision:
        game_over()
        pg.display.flip()
        time.sleep(5)
        break

    # check if victory
    if len(aliens) < 1:
        you_win()
        pg.display.flip()
        time.sleep(5)
        break


    player_x += player_x_change
    background()
    player(x=player_x, y=player_y)
    bullet(bullet_X, bullet_Y)
    bullet2(bullet2_X, bullet2_Y)
    show_score(scoreX, scoreY)
    for al in aliens:
        alien(al[0], al[1])
    pg.display.flip()
    FPS = 60
