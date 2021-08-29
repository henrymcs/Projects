import pygame
import sys
import copy
import random

pygame.init()

WIDTH = 50
SCREEN = pygame.display.set_mode((WIDTH * 17, WIDTH * 15))
clock = pygame.time.Clock()

#EVENTS
SPAWN_NEW = pygame.USEREVENT + 1
SPAWN_NEW_EVENT = pygame.event.Event(SPAWN_NEW)
SPAWN_FRUIT = pygame.USEREVENT + 2
SPAWN_FRUIT_EVENT = pygame.event.Event(SPAWN_FRUIT)

#COLORS
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Snake():
    def __init__(self):
                          
        self.snake_body = [[17//2, 15//2]]

    def move(self, head_direction, new_cube):
        
        old_last_element = copy.deepcopy(self.snake_body[-1])
        
        for cube in range(len(self.snake_body) - 1, -1, -1):
            
            if cube == len(self.snake_body) - 1:
                self.cover(self.snake_body[cube])
            if cube != 0:
             
                self.snake_body[cube] = copy.deepcopy(self.snake_body[cube-1])
            elif cube == 0:
                if head_direction == 'up':
                    self.snake_body[cube][1] -= 1
                if head_direction == 'down':
                    self.snake_body[cube][1] += 1
                if head_direction == 'left':
                    self.snake_body[cube][0] -= 1
                if head_direction == 'right':
                    self.snake_body[cube][0] += 1
        if new_cube:
            self.snake_body.append(old_last_element)

    def cover(self, cube):

        pygame.draw.rect(SCREEN, BLACK, (cube[0] * WIDTH, cube[1] * WIDTH, WIDTH, WIDTH))
        pygame.display.update()

    def delete(self):

        for cube in self.snake_body:
            self.cover(cube)
        self.snake_body = []

    def check_collisions(self):

        collide = False
        self.head = self.snake_body[0]
        if self.head[0] < 0:
            collide = True
        if self.head[0] > 17:
            collide = True
        if self.head[1] < 0:
            collide = True
        if self.head[1] > 15:
            collide = True
        if self.head in self.snake_body[1:]:
            collide = True
        return collide

def draw_snake(snake):
    for section in snake.snake_body:
        pygame.draw.rect(SCREEN, BLUE, (section[0] * WIDTH, section[1] * WIDTH, WIDTH, WIDTH))
        pygame.display.update()

def spawn_fruit(snake):
    fruit = []
    while True:
        fruit = [random.randint(0,17 - 1), random.randint(0,15 - 1)]
        if fruit in snake.snake_body:
            continue
        break
    return fruit

def draw_fruit(fruit):
    pygame.draw.rect(SCREEN, RED, (fruit[0] * WIDTH, fruit[1] * WIDTH, WIDTH, WIDTH))
    pygame.display.update()

def delete_fruit(fruit):
    pygame.draw.rect(SCREEN, BLACK, (fruit[0] * WIDTH, fruit[1] * WIDTH, WIDTH, WIDTH))
    pygame.display.update()

def restart(snake, fruit):
    pygame.time.wait(5000)
    snake.delete()
    delete_fruit(fruit)
    main()

def main():
    snake = Snake()
    fruit = spawn_fruit(snake)
    draw_fruit(fruit)
    direction = 'None'
    game_over = False
    while True:
        print(fruit)
        spawn_new = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SPAWN_FRUIT:
                fruit = spawn_fruit(snake)
                draw_fruit(fruit)
            
            if event.type == SPAWN_NEW:
                spawn_new = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:

                    if len(snake.snake_body) == 1 or direction != 'down':
                        direction = 'up'
                if event.key == pygame.K_a:
                    if len(snake.snake_body) == 1 or direction != 'right':
                        direction = 'left'
                if event.key == pygame.K_s:
                    if len(snake.snake_body) == 1 or direction != 'up':
                        direction = 'down'
                if event.key == pygame.K_d:
                    if len(snake.snake_body) == 1 or direction != 'left':
                        direction = 'right'

        if snake.snake_body[0] == fruit:
            pygame.event.post(SPAWN_FRUIT_EVENT)
            pygame.event.post(SPAWN_NEW_EVENT)
        if direction != 'None' and game_over == False:
            snake.move(direction, spawn_new)

        if snake.check_collisions() == True:
            game_over = True
            restart(snake, fruit)
            break
        draw_snake(snake)
        clock.tick(5)
        
if __name__ == '__main__':
    main()