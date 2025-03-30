#Imports
import random, time
import pygame, sys
from pygame.locals import *

#Initializing and creating the screen
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Setting up FPS
clock = pygame.time.Clock()

running = True

#Variables
SCORE = 0
A_SCORE = 0
SPEED = 2

#Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

#Setting the capture
pygame.display.set_caption("Game")

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_medium = pygame.font.SysFont("Verdana", 35)
game_over = font.render("Game Over", True, BLACK)
game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))

#Background
background = pygame.image.load("AnimatedStreet.png")

#Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if(self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

#Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

#Coin
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("coin.png")
        self.image = self.original_image
        #self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.active = True
        self.reappear_time = 0
        self.size_coin = 1
        self.appear()
    #Size of coins
    def size(self):
        self.size_coin = random.randint(1, 3)
        if self.size_coin == 1:
            new_size = (25, 25)
        elif self.size_coin == 2:
            new_size = (35, 35)
        else:
            new_size = (50, 50)

        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect()
        return self.image
    #The bigger the coin, the bigger the score
    def get_score(self):
        if self.size_coin == 1:
            return 1
        elif self.size_coin == 2:
            return 2
        else: return 3

    def appear(self):
        self.active = True
        self.size()
        self.image.set_alpha(255)
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)

    def hide(self):
        self.active = False
        self.reappear_time = pygame.time.get_ticks() + 3000
        self.image.set_alpha(0)

    def move(self):
        if self.active:
            self.rect.move_ip(0, 4)
            if self.rect.top > SCREEN_HEIGHT:
                self.hide()

        if not self.active and pygame.time.get_ticks() >= self.reappear_time:
            self.appear()

#Setting up Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
coins = pygame.sprite.Group()
coins.add(C1)

#Game loop
while(running):
    # Cycles through all events occuring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background, (0, 0))
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    screen.blit(scores, (SCREEN_WIDTH - 100, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        #Blit everything except a coin or a coin if it is active
        if not isinstance(entity, Coin) or entity.active:
            screen.blit(entity.image, entity.rect)

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        time.sleep(0.5)
        screen.fill(RED)
        screen.blit(game_over, game_over_rect)
        score_text = font_medium.render("Your score is: " + str(SCORE), True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(score_text, score_rect)
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()

        time.sleep(5)
        pygame.quit()
        sys.exit()

    #Scoring and speeding up
    if pygame.sprite.spritecollideany(P1, coins) and C1.active:
        SCORE += C1.get_score()
        A_SCORE += C1.get_score()
        C1.hide()
        #Every 5 points speed up
        if A_SCORE >= 5:
            SPEED += 1
            A_SCORE %= 5

    pygame.display.update()
    clock.tick(60)

pygame.quit()