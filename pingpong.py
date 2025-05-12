import random

import pygame.display
from pygame import *
# from random import *
from time import time as timer
win_height = 700
win_width = 900
win = display.set_mode((win_width, win_height))
display.set_caption('ping pong')
back = (0, 200, 0)
win.fill(back)



# text
font.init()
font1 = font.Font(None, 80)
font = font.Font(None, 35)

lose_txt_red = font1.render("RED LOSES! ", 1, (250, 250, 250))
lose_txt_blue = font1.render("BLUE LOSES! ", 1, (250, 250, 250))
# music
mixer.init()
lose_sound = mixer.Sound('lose_sound.wav')
# mixer.music.set_volume(0.3)
# mixer.music.play()


# class parent
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update_blue(self):
        keys = key.get_pressed()
        if keys[K_s] and self.rect.y < win_height-90:
            self.rect.y += self.speed
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

    def update_red(self):
        keys = key.get_pressed()
        if keys[K_DOWN] and self.rect.y < win_height-90:
            self.rect.y += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = random.randint(70, win_width-70)
            self.rect.y = 0
            lost += 1


# our sprites
player_blue = Player('blue.png', 5, win_height - 100, 60, 90, 10)
player_red = Player('red.png', 840, win_height - 100, 60, 90, 10)
ball = GameSprite('ball.png', win_width/2-25, win_height/2-25, 50, 50, 12)


def reset_ball():
    ball.rect.x = win_width//2-25
    ball.rect.y = win_height//2-25
    return random.choice([-1, 1])*random.randint(3, 5), random.choice([-1, 1])*random.randint(3, 5)


x_speed, y_speed = reset_ball()
game = True
finish = False
clock = time.Clock()
FPS = 60
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        # elif i.type == KEYDOWN:
    if not finish:
        win.fill(back)
        # производим движения спрайтов
        player_red.update_red()
        player_blue.update_blue()
        ball.rect.x += x_speed
        ball.rect.y += y_speed
        if ball.rect.y < 0 or ball.rect.y > win_height-50:
            y_speed *= -1
        if sprite.collide_rect(player_red, ball) or sprite.collide_rect(player_blue, ball):
            x_speed *= -1
        if ball.rect.x < 0:
            finish = True
            lose_sound.play()
            win.blit(lose_txt_blue, (win_width//2-100, win_height//2-50))
            pygame.display.update()
            pygame.time.delay(1505)
            finish = False
            x_speed, y_speed = reset_ball()
        if ball.rect.x > win_width:
            finish = True
            lose_sound.play()
            win.blit(lose_txt_red, (win_width//2-100, win_height//2-50))
            pygame.display.update()
            pygame.time.delay(1505)
            finish = False
            x_speed, y_speed = reset_ball()
        # обновляем их в новом местоположении при каждой итерации цикла
        player_blue.reset()
        player_red.reset()
        ball.reset()
    display.update()
    clock.tick(FPS)