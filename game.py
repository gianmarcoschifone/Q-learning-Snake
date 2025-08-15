from snake import Snake
from food import Food
from direction import Direction
from agent import Agent
import pygame, copy

WINDOW_SIZE = 600
CELL_SIZE = 30
GRID_COLOR = (50, 50, 50)

class Game:
    def __init__(self):
        self.best_score = 0
        self.setup()
    def restart(self):
        self.setup()
    def setup(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False

    def check_if_dead(self, snake):
            head = snake.body[-1]
            wall_hit = head[0] >= 21 or head[1] >= 21 or head[0] <= 0 or head[1] <= 0
            for elem in snake.body[:-1]:
                if head[0] == elem[0] and head[1] == elem[1]:
                    return True
            return wall_hit
    
    def eat(self):
            head = self.snake.body[-1]
            if head[0] == self.food.position[0] and head[1] == self.food.position[1]:
                self.score = self.score + 1
                if self.best_score < self.score:
                    self.best_score = self.score
                self.food = Food(self.snake.body)
                self.snake.growing = True

    def draw_grid(self, screen):
            for x in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_SIZE))
            for y in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_SIZE, y))

    def game_is_over(self, screen):
        font = pygame.font.SysFont(None, 40)
        text_surface = font.render("You're dead! Press any key to restart", True, "red")
        text_rect = text_surface.get_rect()
        text_rect.center = (WINDOW_SIZE // 2, WINDOW_SIZE // 2)
        screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def update_game(self, screen):
        screen.fill("black")
        self.draw_grid(screen)
        self.snake.draw(screen)
        self.food.draw(screen)
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(f"Score: {self.score}   Best score: {self.best_score}", True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        clock = pygame.time.Clock()

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
                self.game_is_over(screen)
            else:
                self.update_game(screen)

                if pygame.time.get_ticks() - last_update_time > 100:
                    self.snake.move()
                    self.game_over = self.check_if_dead(self.snake)
                    self.eat()
                    last_update_time = pygame.time.get_ticks()
                
                pygame.display.flip()

                clock.tick(60)

    #RL
    #booleans: 4 directions, 4 relative positions (food-head), 3 danger relative positions
    def get_state(self):
        def get_future_snake(direction):
            future_snake = copy.deepcopy(self.snake)
            head = future_snake.body[-1]
            future_head = (head[0]+direction.value[0], head[1]+direction.value[1])
            future_snake.body.append(future_head)
            if (not future_snake.growing):
                future_snake.body.pop(0)
            return future_snake

        head = self.snake.body[-1]
        state = []
        #snake's direction is left/right/up/down
        state.append(int(self.snake.direction == Direction.LEFT))
        state.append(int(self.snake.direction == Direction.RIGHT))
        state.append(int(self.snake.direction == Direction.UP))
        state.append(int(self.snake.direction == Direction.DOWN))
        #food is left/right/up/down
        state.append(int(self.food.position[0] < head[0]))
        state.append(int(self.food.position[0] > head[0]))
        state.append(int(self.food.position[1] < head[1]))
        state.append(int(self.food.position[1] > head[1]))
        #danger is straight/left/right
        future_snake = get_future_snake(self.snake.direction)
        state.append(int(self.check_if_dead(future_snake)))
        future_snake = get_future_snake(Direction.LEFT)
        state.append(int(self.check_if_dead(future_snake)))
        future_snake = get_future_snake(Direction.RIGHT)
        state.append(int(self.check_if_dead(future_snake)))
        return tuple(state)
    
    def step(self, action):
        action = [self.snake.turnLeft, self.snake.turnRight, self.snake.turnUp, self.snake.turnDown][action]
        action()
        self.snake.move()
        self.game_over = self.check_if_dead(self.snake)
        self.eat()

        reward = -0.2
        if self.game_over:
            reward = -10
        elif self.snake.growing:
            reward = 1
        return reward, self.get_state(), self.game_over
    
    def rl_start(self, agent):
        agent.stop_exploration()
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and self.game_over:
                    self.restart()

            state = self.get_state()
            action = agent.get_action(state)
            action = [self.snake.turnLeft, self.snake.turnRight, self.snake.turnUp, self.snake.turnDown][action]
            action()

            if self.game_over:
                self.game_is_over(screen)
            else:
                self.update_game(screen)

                self.snake.move()
                self.game_over = self.check_if_dead(self.snake)
                self.eat()
                
                pygame.display.flip()

                clock.tick(60)


    pygame.quit()