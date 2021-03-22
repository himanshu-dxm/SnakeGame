#The Snake Game using Pygame

import pygame,sys,random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False
    
    def draw_snake(self):
        for block in self.body:
            x_pos = block.x * cell_size
            y_pos =block.y * cell_size 
            block_rect = pygame.Rect(x_pos , y_pos , cell_size , cell_size)
            pygame.draw.rect(screen,(183,111,122),block_rect)
    
    def move_snake(self):
        
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction )
            self.body = body_copy[:]
            self.new_block = False            
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction )
            self.body = body_copy[:]
    
    def add_block(self):
        self.new_block = True


class FRUIT:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size , self.pos.y * cell_size , cell_size , cell_size) #creating a rectangle
        #screen.blit(apple,fruit_rect)#for adding image as a fruit
        pygame.draw.rect(screen,(126,166,114),fruit_rect)#surface,color,rectangle as arguments
    
    def randomize(self):
        self.x = random.randint(0,cell_number - 1) #creating x,y positions
        self.y = random.randint(0,cell_number - 1) #drwaing a square
        self.pos = Vector2(self.x,self.y) 



class MAIN:
    def __init__(self):
        self.snake = SNAKE()#creating our snake 
        self.fruit = FRUIT()#creating a fruit object
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # 2 things to be done when the collide
            # -> change fruit location and -> add another block to snake
            self.fruit.randomize()# 1 done by this method
            self.snake.add_block()
            
            for block in self.snake.body[1:]:#this is makig sure fruit dosent overlaps snake body
                if block == self.fruit.pos:
                    self.fruit.randomize()
                
    
    def check_fail(self):
        # 2 consditions when game over
        # -> when snake hits itself -> when it hits wall
        
        #checking wall hit
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        
        #checking self hit
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
        
    def game_over(self):
        pygame.quit()
        sys.exit()
    
    def draw_grass(self):
        grass_color = (167,209,61)
        
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size , row * cell_size , cell_size , cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size , row * cell_size , cell_size , cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
    
    def draw_score(self):
        score_text = str((len(self.snake.body)-3)*10)
        score_surface = game_font.render(score_text , True , (56,76,12))#render(text,antiAliasing,color) 
        score_x = int(cell_size * cell_number - 60 )
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        bg_rect  = pygame.Rect(score_rect.left-5,score_rect.top-5,score_rect.width+10,score_rect.height+10)
        
        pygame.draw.rect(screen,(56,74,12),bg_rect,2)
        screen.blit(score_surface,score_rect)               
                


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number , cell_size * cell_number))
clock = pygame.time.Clock()
#apple = pygame.image.load('appleImg.jpg').convert_alpha()# this is for adding image as fruit
game_font = pygame.font.Font(None,25)#creating a new font object for placing text in game

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT#creating a user defined event
pygame.time.set_timer(SCREEN_UPDATE,150)#150ms


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
    
    screen.fill((175,215,70))
    
    main_game.draw_elements()
    
    pygame.display.update()
    clock.tick(60)
