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
score_red = 0
score_blue = 0

lose_txt_red = font1.render("POINT FOR BLUE! ", 1, (250, 250, 250))
lose_txt_blue = font1.render("POINT FOR RED! ", 1, (250, 250, 250))
final_lose_txt_red = font1.render("RED LOSES! ", 1, (250, 250, 250))
final_lose_txt_blue = font1.render("BLUE LOSES! ", 1, (250, 250, 250))
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


class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.original_image = self.image.copy()
        self.angle = 0
        self.spin_speed = 0

    def update_spin(self, x_speed, y_speed):
        self.spin_speed *= 0.95
        self.spin_speed += (abs(x_speed)+abs(y_speed))*0.02

    def spin_hit(self, offset):
        self.spin_speed += offset*5

    def reset(self):
        self.angle = (self.angle + self.spin_speed) % 360
        self.image = transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        win.blit(self.image, self.rect)
# our sprites


player_blue = Player('blue.png', 5, win_height - 100, 60, 90, 10)
player_red = Player('red.png', 840, win_height - 100, 60, 90, 10)
ball = Ball('ball.png', win_width/2-25, win_height/2-25, 50, 50, 12)


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
            y_speed *= -1.00001
            # столкновение с ракеткой blue

        if sprite.collide_rect(player_blue, ball):
            ball.rect.left = player_blue.rect.right  # предотвращаем залипание
            x_speed *= -1  # отражение по X
            offset = (ball.rect.centery - player_blue.rect.centery)/(player_blue.rect.height/2)
            y_speed += offset*2
            ball.spin_hit(offset)

        # столкновение с ракеткой red

        if sprite.collide_rect(player_red, ball):
            ball.rect.right = player_red.rect.left  # предотвращаем залипание
            offset = (ball.rect.centery - player_red.rect.centery)/(player_red.rect.height/2)
            y_speed += offset*2
            x_speed *= -1
            ball.spin_hit(offset)
        if ball.rect.x < 0:
            score_red += 1
            if score_red >= 5:
                finish = True
                win.blit(final_lose_txt_blue, (win_width//2-200, win_height//2-50))
            else:

                lose_sound.play()
                win.blit(lose_txt_blue, (win_width//2-200, win_height//2-50))
            pygame.display.update()
            pygame.time.delay(1505)
            x_speed, y_speed = reset_ball()
        if ball.rect.x > win_width:
            score_blue += 1
            if score_blue >= 5:
                finish = True
                win.blit(final_lose_txt_red, (win_width//2-200, win_height//2-50))
            else:
                lose_sound.play()
                win.blit(lose_txt_red, (win_width//2-200, win_height//2-50))
            pygame.display.update()
            pygame.time.delay(1505)
            x_speed, y_speed = reset_ball()
        # обновляем их в новом местоположении при каждой итерации цикла
        ball.update_spin(x_speed, y_speed)
        player_blue.reset()
        player_red.reset()
        ball.reset()
        score_txt = font1.render(f"BLUE:{score_blue} | RED:{score_red}", 1, (255, 255, 255))
        score_txt.set_alpha(127)
        win.blit(score_txt, (win_width//2-200, 30))
    display.update()
    clock.tick(FPS)
