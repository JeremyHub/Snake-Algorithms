# snake game with pygame
import pygame
import random
import snake_ai
import logging

class Board:
    def __init__(self, width, height, screen, screen_size, move_limit, debug=False, does_draw=True, log_moves=False):
        self.does_draw = does_draw
        self.move_limit = move_limit
        self.debug = debug
        self.width = width
        self.screen = screen
        self.height = height
        self.log_moves = log_moves
        self.recreating = False
        if self.log_moves:
            self.foods = []
            self.moves = []
        self.food = None
        self.direction = 'right'
        self.score = 0
        self.num_moves = 0
        self.scale = screen_size//max(width,height) - 10
        self.padding = self.scale//5
        self.action_queue = []
        self.game_over = False
        self.reset()

    def generate_food(self):
        possible_squares = []
        for x in range(self.width):
            for y in range(self.height):
                possible_squares.append((x, y))
        for x, y in self.snake:
            possible_squares.remove((x, y))
        if len(possible_squares) == 0:
            if self.debug: logging.info("could not generate food")
            return False
        self.food = random.choice(possible_squares)
        if self.log_moves: self.foods.append(self.food)
        return True

    def move_snake(self):
        head = self.snake[0]
        if self.direction == 'right':
            new_head = (head[0] + 1, head[1])
        elif self.direction == 'left':
            new_head = (head[0] - 1, head[1])
        elif self.direction == 'up':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'down':
            new_head = (head[0], head[1] + 1)
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            if not self.generate_food():
                self.win()
            return True
        else:
            self.snake.pop()
            return False

    def win(self):
        self.game_over = True
    
    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= self.width:
            self.game_over = True
        if head[1] < 0 or head[1] >= self.height:
            self.game_over = True
        if head in self.snake[1:]:
            self.game_over = True
    
    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 255), (self.snake[0][0] * self.scale + self.padding, self.snake[0][1] * self.scale + self.padding, self.scale - (self.padding), self.scale - (self.padding)))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.snake[-1][0] * self.scale + self.padding, self.snake[-1][1] * self.scale + self.padding, self.scale - (self.padding), self.scale - (self.padding)))        
        transition_stage = 0
        g = 0
        b = 255
        for x, y in self.snake[1:len(self.snake)-1]:
            if transition_stage == 0:
                g += 255//(len(self.snake)-2)
                if g >= 255:
                    transition_stage = 2
            elif transition_stage == 2:
                b += 255//(len(self.snake)-2)
                if b >= 255:
                    transition_stage = 3
            elif transition_stage == 3:
                g -= 255//(len(self.snake)-2)
                if g <= 0:
                    transition_stage = 5
            elif transition_stage == 5:
                b -= 255//(len(self.snake)-2)
                if b <= 0:
                    transition_stage = 0
            pygame.draw.rect(self.screen, (0, g, b), (x * self.scale + self.padding, y * self.scale + self.padding, self.scale - (self.padding), self.scale - (self.padding)))
        
        pygame.draw.rect(self.screen, (255, 0, 0), (self.food[0] * self.scale + self.padding, self.food[1] * self.scale + self.padding, self.scale - (self.padding), self.scale - (self.padding)))

        # draw score
        font = pygame.font.SysFont('Arial', 20)
        text = font.render('Score: ' + str(self.score), True, (255, 255, 255))
        self.screen.blit(text, (0, self.height * self.scale))
        
        # draw grid lines
        for x in range(self.width + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (x * self.scale, 0), (x * self.scale, self.height * self.scale), 1)
        for y in range(self.height + 1):
            pygame.draw.line(self.screen, (255, 255, 255), (0, y * self.scale), (self.width * self.scale, y * self.scale), 1)
        pygame.display.flip()

        self.draw_heuristics()

        pygame.display.update()

    def draw_heuristics(self):
        font = pygame.font.SysFont('Arial', 20)
        text = font.render(f'num moves: {self.num_moves}', True, (255, 255, 255))
        self.screen.blit(text, (80, self.height * self.scale))
        pygame.display.flip()
    
    def handle_input(self, input):
        if input == 'right' and self.direction != 'left':
            self.direction = 'right'
        elif input == 'left' and self.direction != 'right':
            self.direction = 'left'
        elif input == 'up' and self.direction != 'down':
            self.direction = 'up'
        elif input == 'down' and self.direction != 'up':
            self.direction = 'down'
    
    def update(self):
        if self.debug: logging.info(f'updated: {self.num_moves} {self.direction}')
        if self.log_moves: self.moves.append(self.direction)
        ate_food = self.move_snake()
        self.check_collision()
        if self.does_draw and not self.recreating: self.draw()
        self.num_moves += 1
        return ate_food
    
    def run_with_human_input(self):
        assert self.does_draw
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.action_queue.append('right')
                elif event.key == pygame.K_LEFT:
                    self.action_queue.append('left')
                elif event.key == pygame.K_UP:
                    self.action_queue.append('up')
                elif event.key == pygame.K_DOWN:
                    self.action_queue.append('down')
                elif event.key == pygame.K_SPACE:
                    self.reset()
        if len(self.action_queue) > 0:
            for action in self.action_queue:
                self.handle_input(action)
                self.update()
                pygame.time.delay(120)
            self.action_queue = []
        else:
            self.update()
            pygame.time.delay(120)
        if self.game_over:
            result = (self.score, self.num_moves)
            self.reset()
            return result
        
    def reset(self):
        if self.debug: logging.info('reset')
        self.snake = [(self.width // 2, self.height // 2)]
        tail = (self.snake[0][0] + 1, self.snake[0][1])
        self.snake.append(tail)
        # tail2 = (self.snake[0][0] + 2, self.snake[0][1])
        # self.snake.append(tail2)
        self.direction = 'right'
        self.score = len(self.snake)
        self.num_moves = 0
        self.game_over = False
        self.generate_food()
    
    def run_with_ai_input(self):
        self.direction = snake_ai.get_action(self.snake, self.food, (self.width, self.height))
        if self.debug: logging.info(f'ai action: {self.direction}')
        self.update()
        if self.num_moves > self.move_limit or self.game_over:
            to_return = (self.score, self.num_moves)
            if self.debug: logging.info(f'game over: {to_return}')
            self.reset()
            return to_return
        return None
    
    def reconstruct_game(self, moves, foods):
        self.log_moves = False
        self.does_draw = True
        self.reset()
        self.recreating = True
        self.food = foods.pop(0)
        for move in moves:
            self.direction = move
            if self.update() and len(self.food)>0: self.food = foods.pop(0)
            self.draw()
            pygame.time.delay(30)
