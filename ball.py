import pyray as pr
import math

class Ball:
    def __init__(self, initial_position, initial_direction, radius, speed):
        self.initial_position = pr.Vector2(initial_position.x, initial_position.y)
        self.initial_direction = initial_direction
        
        self.position = pr.Vector2(initial_position.x, initial_position.y)
        self.direction = initial_direction
        self.radius = radius
        self.speed = speed
        self.color = pr.GRAY

    def reset(self, player_paddle_rect):
        self.position.x = player_paddle_rect.x + (player_paddle_rect.width / 2)
        self.position.y = player_paddle_rect.y - self.radius - 1
        self.direction = self.initial_direction

    def move(self):
        dir_rad = math.radians(self.direction)
        self.position.x += self.speed * math.cos(dir_rad)
        self.position.y += self.speed * math.sin(dir_rad)

    def check_wall_collision(self, screen_width, screen_height):
        collided_boundary = False
        if self.position.x - self.radius <= 0:
            self.position.x = self.radius
            self.direction = 180.0 - self.direction
            collided_boundary = True
        elif self.position.x + self.radius >= screen_width:
            self.position.x = screen_width - self.radius
            self.direction = 180.0 - self.direction
            collided_boundary = True
        
        if self.position.y - self.radius <= 0:
            self.position.y = self.radius
            self.direction = -self.direction
            collided_boundary = True
        elif self.position.y + self.radius >= screen_height:
            return "bottom_wall_hit"
        
        return "collided_other_wall" if collided_boundary else None

    def draw(self):
        pr.draw_circle_v(self.position, self.radius, self.color)