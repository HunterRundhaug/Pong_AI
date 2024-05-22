import pygame
import random
import math

class PongGame:
    def __init__(self, screen_width=1000, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pong")

        # Main Game Objects -------
        # player is Right side opponent is Left side
        self.ball = pygame.Rect((self.screen_width / 2 - 15, self.screen_height / 2 - 15, 30, 30))
        self.player = pygame.Rect((self.screen_width - 15, self.screen_height / 2 - 60, 15, 120))
        self.opponent = pygame.Rect((0, self.screen_height / 2 - 60, 15, 120))

        # Text for the Score ------
        self.text = "0"
        self.font = pygame.font.Font(None, 25)
        self.text_color = (255, 255, 255)  # White
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        #--------------------------

        # Game Variables ----------
        self.ball_speed_x_const = 15
        self.ball_speed_y_const = 15
        self.ball_speed_x = self.ball_speed_x_const
        self.ball_speed_y = self.ball_speed_y_const
        self.player_speed = 12 #10
        self.p1_hits = 0
        self.p2_hits = 0
        self.p1_miss = 0
        self.p2_miss = 0
        self.current_rally = 0
    
    def update(self):
        self.text = str(self.current_rally)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.draw_items()
        self.move_ball()

    def update_train_mode(self):
        self.text = str(self.current_rally)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.move_ball()

    def draw_items(self):
        self.screen.fill((50,50,50)) # Clear last frame
        pygame.draw.aaline(self.screen, (0,0,0), (self.screen_width/2, 0), (self.screen_width/2, self.screen_height))
        pygame.draw.ellipse(self.screen, (255,50,50), self.ball)
        pygame.draw.rect(self.screen, (10, 200, 100), self.player)
        pygame.draw.rect(self.screen, (200, 100, 10), self.opponent)
        self.screen.blit(self.text_surface, self.text_rect)
        
        pygame.display.update() # Update the frame

    def move_player_1(self, direction=0): # Player 1 Movement
        if direction == 1 and self.player.top >= 0:
            self.player.y -= self.player_speed
            #self.player.move_ip((0,-self.player_speed)) # Move Up
            
        elif direction == -1 and self.player.bottom <= self.screen_height:
            #self.player.move_ip((0, self.player_speed)) # Move Down
            self.player.y += self.player_speed
        
        else: # return false if trying to move paddle off screen
            return False

    def move_player_2(self, direction=0): # Player 2 Movement
        if direction == 1 and self.opponent.top >= 0:
            #self.opponent.move_ip((0,-self.player_speed)) # Move Up
            self.opponent.y -= self.player_speed

        elif direction == -1 and self.opponent.bottom <= self.screen_height:
            #self.opponent.move_ip((0, self.player_speed)) # Move Down
            self.opponent.y += self.player_speed
        
        else: # return false if trying to move paddle off screen
            return False
    
    def move_ball(self):

            # Determine Ball Collisions
        if self.ball.bottom >= self.screen_height or self.ball.top <= 0:
            self.ball_speed_y *= -1
            self.ball_speed_x += random.uniform(-.1, .1)  # Adjust the range as needed
            self.ball_speed_y += random.uniform(-0.5, .5)  # Adjust the range as needed
        if self.ball.left <= 0: # Ball Out of Bounds Left
            self.p2_miss += 1
            self.ball_restart()
        if self.ball.right >= self.screen_width: # Ball Out of Bounds Right
            self.p1_miss += 1
            self.ball_restart()

        if self.ball.colliderect(self.player):
            self.ball_speed_x *= -1
            # Add randomness to the ball's speed and angle after hitting the opponent's paddle
            self.ball_speed_x += random.uniform(-.1, .1)  # Adjust the range as needed
            self.ball_speed_y += random.uniform(-0.5, .5)  # Adjust the range as needed
            self.p1_hits += 1
            self.current_rally += 1

        elif self.ball.colliderect(self.opponent):
            self.ball_speed_x *= -1
            self.ball.x += self.ball_speed_x  # Ensure the ball is placed outside the paddle to avoid sticking
            # Add randomness to the ball's speed and angle after hitting the opponent's paddle
            self.ball_speed_x += random.uniform(-.1, .1)  # Adjust the range as needed
            self.ball_speed_y += random.uniform(-0.5, .5)  # Adjust the range as needed
            self.p2_hits += 1
            self.current_rally += 1

        self.fix_ball_speed()

        # Move ball after calulations
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        return angle
    
    def fix_ball_speed(self): 
        # Keep ball_speed_x within a range 1 above or below ball_speed_x_const
        if self.ball_speed_x < 0:
            if self.ball_speed_x < -self.ball_speed_x_const - 1:
                self.ball_speed_x = -self.ball_speed_x_const - 1
        else:
            if self.ball_speed_x > self.ball_speed_x_const + 1:
                self.ball_speed_x = self.ball_speed_x_const + 1

        # Keep ball_speed_y within a range 1 above or below ball_speed_y_const
        if self.ball_speed_y < 0:
            if self.ball_speed_y < -self.ball_speed_y_const - 2:
                self.ball_speed_y = -self.ball_speed_y_const - 2
        else:
            if self.ball_speed_y > self.ball_speed_y_const + 2:
                self.ball_speed_y = self.ball_speed_y_const + 2

    def ball_restart(self): # Reset ball when it goes out of bounds
        self.ball.center = (self.screen_width / 2 - 15, self.screen_height / 2 - 15)
        angle = self._get_random_angle(-50, 50, [0])
        self.ball_speed_y = math.sin(angle) * self.ball_speed_y_const
        self.ball_speed_x = -abs(math.cos(angle) * self.ball_speed_x_const)
        
        self.current_rally = 0
            

        

    
        