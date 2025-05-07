import pyray as pr

class Ball:
    def __init__(self, position: pr.Vector2, direction):
        self.position = position
        self.direction = direction
        self.color = pr.GRAY

    def draw(self):
        pr.draw_circle_v(
            self.position,
            5, #size
            self.color
            )

    def update(self, position, direction):
        self.position = position
        self.direction = direction
        
