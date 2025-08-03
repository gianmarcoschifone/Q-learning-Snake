from direction import Direction
import pygame

#-->
class Snake:
    def __init__(self):
        self.body = [(9, 10), (10, 10), (11, 10)]
        self.direction = Direction.RIGHT
        self.direction_queue = []
        self.growing = False
    def move(self):
        head = self.body[-1]
        if len(self.direction_queue) > 0:
            self.direction = self.direction_queue.pop(0)
        newHead = (head[0]+self.direction.value[0], head[1]+self.direction.value[1])
        self.body.append(newHead)
        if (not self.growing):
            self.body.pop(0)
        else:
            self.growing = False

    def turnUp(self):
        next_direction = self.direction_queue[0] if self.direction_queue else self.direction
        if next_direction != Direction.DOWN:
            self.direction_queue.append(Direction.UP)
    def turnDown(self):
        next_direction = self.direction_queue[0] if self.direction_queue else self.direction
        if next_direction != Direction.UP:
            self.direction_queue.append(Direction.DOWN)
    def turnRight(self):
        next_direction = self.direction_queue[0] if self.direction_queue else self.direction
        if next_direction != Direction.LEFT:
            self.direction_queue.append(Direction.RIGHT)
    def turnLeft(self):
        next_direction = self.direction_queue[0] if self.direction_queue else self.direction
        if next_direction != Direction.RIGHT:
            self.direction_queue.append(Direction.LEFT)
    def draw(self, screen):
        for elem in self.body:
            pygame.draw.rect(screen, (16, 141, 37), ((elem[0]-1)*30, (elem[1]-1)*30, 30, 30))