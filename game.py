from snake import Snake
from food import Food
from direction import Direction
import pygame

WINDOW_SIZE = 600
CELL_SIZE = 30
GRID_COLOR = (50, 50, 50)

class Game:
    def __init__(self):
        self.best_score = 0
        self.setup()
    def restart(self):
        #self.best_score = max(self.best_score, self.score)
        self.setup()
    def setup(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        clock = pygame.time.Clock()

        def draw_grid():
            for x in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_SIZE))
            for y in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_SIZE, y))

        def check_if_dead():
            head = self.snake.body[-1]
            wall_hit = head[0] >= 21 or head[1] >= 21 or head[0] <= 0 or head[1] <= 0
            for elem in self.snake.body[:-1]:
                if head[0] == elem[0] and head[1] == elem[1]:
                    return True
            return wall_hit

        def eat():
            head = self.snake.body[-1]
            if head[0] == self.food.position[0] and head[1] == self.food.position[1]:
                self.score = self.score + 1
                if self.best_score < self.score:
                    self.best_score = self.score
                self.food = Food(self.snake.body)
                self.snake.growing = True

        last_update_time = pygame.time.get_ticks()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        self.restart()
                    elif event.key == pygame.K_w:
                        self.snake.turnUp()
                    elif event.key == pygame.K_s:
                        self.snake.turnDown()
                    elif event.key == pygame.K_a:
                        self.snake.turnLeft()
                    elif event.key == pygame.K_d:
                        self.snake.turnRight()

            if self.game_over:
                font = pygame.font.SysFont(None, 40)
                text_surface = font.render("You're dead! Press any key to restart", True, "red")
                text_rect = text_surface.get_rect()
                text_rect.center = (WINDOW_SIZE // 2, WINDOW_SIZE // 2)
                screen.blit(text_surface, text_rect)
                pygame.display.flip()
            else:
                screen.fill("black")
                draw_grid()
                self.snake.draw(screen)
                self.food.draw(screen)
                font = pygame.font.SysFont(None, 36)
                text_surface = font.render(f"Score: {self.score}   Best score: {self.best_score}", True, (255, 255, 255))
                screen.blit(text_surface, (10, 10))

                if pygame.time.get_ticks() - last_update_time > 150:
                    self.snake.move()
                    self.game_over = check_if_dead()
                    eat()
                    last_update_time = pygame.time.get_ticks()
                
                pygame.display.flip()

                clock.tick(60)

        pygame.quit()