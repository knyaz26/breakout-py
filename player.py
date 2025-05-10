import pyray as pr
from input import Input

class Player:
    def __init__(self, initial_position, width, height, speed):
        self.initial_position = pr.Vector2(initial_position.x, initial_position.y)
        self.position = pr.Vector2(initial_position.x, initial_position.y)
        self.width = width
        self.height = height
        self.speed = speed
        self.size = pr.Rectangle(self.position.x, self.position.y, self.width, self.height)
        self.color = pr.WHITE

    def reset(self):
        self.position = pr.Vector2(self.initial_position.x, self.initial_position.y)
        self._update_rect()

    def _update_rect(self):
        self.size = pr.Rectangle(self.position.x, self.position.y, self.width, self.height)

    def move(self, screen_width):
        if Input.is_action_pressed("ui_left"):
            self.position.x -= self.speed
        elif Input.is_action_pressed("ui_right"):
            self.position.x += self.speed

        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > screen_width - self.width:
            self.position.x = screen_width - self.width
        
        self._update_rect()

    def draw(self):
        pr.draw_rectangle_rec(self.size, self.color)