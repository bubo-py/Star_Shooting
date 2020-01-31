import pygame
from pygame import mixer
import random
import math
import time


# Initialize packages
mixer.init()
pygame.init()



# Setting screen size
screen = pygame.display.set_mode((800, 600))


# Game name, pictures and sounds
pygame.display.set_caption("Star Shooting") # title of the game

icon = pygame.image.load('ufo.png') # icon of the game
pygame.display.set_icon(icon) # setting icon for above icon

background = pygame.image.load('background.png') # background picture

mixer.music.load("background.ogg")
mixer.music.play(-1)


# Player stuff
playerImage = pygame.image.load('player_ship.png')
playerX = 370
playerY = 480
playerX_change = 0


# Enemy stuff
enemyImage = []
enemyX = [] 
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_max = 6

for i in range(enemy_max):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)


# Bullet stuff

# Ready - you can't see the bullet on the screen
# Fire - the bullet is currently moving
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

# Score display stuff
score_value = 0
font = pygame.font.Font('orange_juice_2.0.ttf', 45)

textX = 10
textY = 10

# Game losing text
game_over_font = pygame.font.Font('orange_juice_2.0.ttf', 100)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 102, 153))
    screen.blit(score, (x, y))

def game_lose_text():
    game_over_text = game_over_font.render('GAME OVER', True, (77, 184, 255))
    screen.blit(game_over_text, (150, 250))

def player(x, y):
    screen.blit(playerImage, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))

def shoot_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    d = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if d < 27:
        return True
    else:
        return False


# Game loop
running = True
# looping the window(game) to not dissapear after starting program
while running:
    
    # RGB collor of screen background
    screen.fill((0, 0, 170))

    # Background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get(): # looping through events
        
        if event.type == pygame.QUIT:
            running = False
        
        # movements of the player by keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1.2
            
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.2
            
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser_sound.wav')
                    bullet_sound.play()
                    bulletX = playerX # get current x cord of player
                    shoot_bullet(bulletX, bulletY)
            
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Player borders
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    enemyX += enemyX_change

    # Enemy movement
    for i in range(enemy_max):
        # losing the game
        if enemyY[i] > 440:
            for j in range(enemy_max):
                enemyY[j] = 2000
            game_lose_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

            # Collision stuff
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion_sound.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            
        enemy(enemyX[i], enemyY[i], i)


    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        shoot_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    
    pygame.display.update()

