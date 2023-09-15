#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 11:45:15 2017

@author: apple
"""

import pygame as pg
import random as rnd
from math import fabs

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)

scree_size = width, height = 800, 600

part_size = 10

dx = part_size
dy = 0

length = 5
dir = 'r'
difficulty = 7

snake_parts = []
snake_sprites = pg.sprite.Group()
obstacle_sprites = pg.sprite.Group()
food_sprite = pg.sprite.Group()
head_sprite = pg.sprite.Group()
pg.init()
screen = pg.display.set_mode((width, height + 20))
pg.display.set_caption('Snake')
clock = pg.time.Clock()
highscore = 0

"""with open('scores', 'r') as file:
    highscore = int(file.read())"""


class Part(pg.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pg.Surface((part_size, part_size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Obstacle(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Food(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def snake_init():
    for i in range(length):
        x = 500 - i * part_size
        y = 30
        if i == 0:
            part = Part(x, y, RED)
        else:
            part = Part(x, y, WHITE)
        snake_parts.append(part)
        if i > 0:
            snake_sprites.add(part)
        elif i == 0:
            head_sprite.add(part)


def wall_init():
    Wall = list()
    Wall.append(Obstacle(0, 0, 10, height, ORANGE))
    Wall.append(Obstacle(0, 0, width, 10, ORANGE))
    Wall.append(Obstacle(width - 10, 0, 10, height, ORANGE))
    Wall.append(Obstacle(0, height - 10, width, 10, ORANGE))
    for wall in Wall:
        obstacle_sprites.add(wall)


def obstacles_init():
    obstacles = list()
    obstacles.append(Obstacle(70, 70, 150, 10, BLUE))
    obstacles.append(Obstacle(70, 70, 10, 150, BLUE))
    obstacles.append(Obstacle(70, 370, 10, 150, BLUE))
    obstacles.append(Obstacle(70, 520, 150, 10, BLUE))
    obstacles.append(Obstacle(570, 70, 150, 10, BLUE))
    obstacles.append(Obstacle(720, 70, 10, 150, BLUE))
    obstacles.append(Obstacle(720, 370, 10, 150, BLUE))
    obstacles.append(Obstacle(570, 520, 160, 10, BLUE))
    obstacles.append(Obstacle(200, 150, 400, 10, BLUE))
    obstacles.append(Obstacle(200, 440, 400, 10, BLUE))
    for obstacle in obstacles:
        obstacle_sprites.add(obstacle)


def food_gen():
    done = False
    while not done:
        x = rnd.randrange(width)
        y = rnd.randrange(height)
        food = Food(x, y, 10, 10, GREEN)
        done = True
        obstacles_collisions = pg.sprite.spritecollide(food, obstacle_sprites, False)
        if obstacles_collisions:
            done = False
        snake_collisions = pg.sprite.spritecollide(food, snake_sprites, False)
        if snake_collisions:
            done = False
        head_collisions = pg.sprite.spritecollide(food, head_sprite, False)
        if head_collisions:
            done = False
    food = Food(x, y, 10, 10, GREEN)
    food_sprite.add(food)


def gameover(score):
    global highscore
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            elif event.type == pg.KEYDOWN:
                run = False
                break
        screen.fill(BLACK)
        if score > highscore:
            with open('scores', 'w') as file:
                highscore = score
                file.write(str(highscore))
        font = pg.font.SysFont('Courier', 85, True, False)
        gameovertxt = font.render("Game Over :(", True, RED)
        font = pg.font.SysFont('Calibri', 70, False, True)
        scoretxt = font.render("Your Score: " + str(score), True, YELLOW)
        font = pg.font.SysFont('Calibri', 50, False, True)
        highscoretxt = font.render("High score: " + str(highscore), True, GREEN)
        font = pg.font.SysFont('Tahoma', 15, False, True)
        presskey = font.render("Press any key to exit...", True, WHITE)
        screen.blit(scoretxt, (230, 250))
        screen.blit(gameovertxt, (100, 100))
        screen.blit(highscoretxt, (270, 320))
        screen.blit(presskey, (320, 590))
        pg.display.flip()
        clock.tick(60)
    pg.quit()


def controller(pause):
    global dx, dy, dir, difficulty
    run = True
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT and not dir == 'r':
                dx = part_size * -1
                dy = 0
                dir = 'l'
            elif event.key == pg.K_RIGHT and not dir == 'l':
                dx = part_size
                dy = 0
                dir = 'r'
            elif event.key == pg.K_UP and not dir == 'd':
                dx = 0
                dy = part_size * -1
                dir = 'u'
            elif event.key == pg.K_DOWN and not dir == 'u':
                dx = 0
                dy = part_size
                dir = 'd'
            elif event.key == pg.K_h:
                difficulty += 1
            elif event.key == pg.K_g:
                if difficulty > 7:
                    difficulty -= 1
            elif event.key == pg.K_p:
                pause = not pause
    return run, pause


def move(eaten, head):
    if not eaten:
        old_part = snake_parts.pop()
        snake_sprites.remove(old_part)
        eaten = False
    x = snake_parts[0].rect.x + dx
    y = snake_parts[0].rect.y + dy
    part = Part(x, y, RED)
    if head:
        old_part = Part(head.rect.x, head.rect.y, WHITE)
        snake_sprites.add(old_part)
        snake_parts.remove(head)
        snake_parts.insert(0, old_part)
        head_sprite.remove(head)
    head = part
    snake_parts.insert(0, part)
    head_sprite.add(part)
    return eaten, head


def collision_handler(eaten, score):
    global length
    run = True
    obstacles_collisions = pg.sprite.spritecollide(snake_parts[0], obstacle_sprites, False)
    if obstacles_collisions:
        run = False
    snake_collisions = pg.sprite.spritecollide(snake_parts[0], snake_sprites, False)
    if snake_collisions:
        run = False
    food_collisions = pg.sprite.spritecollide(snake_parts[0], food_sprite, True)
    if food_collisions:
        eaten = True
        score += 1
        length += 1
        print(score)
        food_gen()
    else:
        eaten = False
    return run, eaten, score


def show(score):
    font = pg.font.SysFont('Calibri', 23, False, False)
    text = font.render("Score: " + str(score), True, WHITE)
    text2 = font.render("High score: " + str(highscore), True, WHITE)
    text3 = font.render("Difficulty: " + str(difficulty) + "        (change it by 'g' and 'h')", True, WHITE)
    screen.blit(text, (10, height + 3))
    screen.blit(text2, (200, height + 3))
    screen.blit(text3, (350, height + 3))
    snake_sprites.draw(screen)
    obstacle_sprites.draw(screen)
    food_sprite.draw(screen)
    head_sprite.draw(screen)
    pg.display.flip()

def level2(Score):
    global dx, dy, dir
    score = Score
    snake_sprites.empty()
    head_sprite.empty()
    obstacle_sprites.empty()
    food_sprite.empty()
    snake_parts.clear()
    snake_init()
    wall_init()
    obstacles_init()
    food_gen()
    pause = True
    run = True
    eaten = False
    head = snake_parts[0]
    dx = part_size
    dy = 0
    dir = 'r'
    while run:
        show(score)
        Run, pause = controller(pause)
        if not pause:
            run, eaten, score = collision_handler(eaten, score)
            eaten, head = move(eaten, head)
        run &= Run
        screen.fill(BLACK)
        clock.tick(difficulty)
    gameover(score)


def level1():
    snake_init()
    wall_init()
    food_gen()
    run = True
    eaten = False
    head = snake_parts[0]
    score = 0
    lvl2 = False
    pause = True
    while run:
        show(score)
        Run, pause = controller(pause)
        if not pause:
            run, eaten, score = collision_handler(eaten, score)
            eaten, head = move(eaten, head)
        screen.fill(BLACK)
        clock.tick(difficulty)
        run &= Run
        if score == 3:
            lvl2 = True
            break
    if lvl2 and run:
        level2(score)
    elif not run:
        gameover(score)
level1()
