import random, pygame

class Food:
    def __init__(self, snake_body):
        self.position = (random.randint(1, 20), random.randint(1, 20))
        while self.position in snake_body:
            self.position = (random.randint(1, 20), random.randint(1, 20))
    def draw(self, screen):
        pygame.draw.circle(screen, (243, 11, 11), ((self.position[0]-1)*30+15, (self.position[1]-1)*30+15), 10)