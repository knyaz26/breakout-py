import pyray as pr

class Player:
    def __init__(self, position):
        self.position = position
        self.size = pr.Rectangle(self.position.x, self.position.y, 50, 15)
        self.color = pr.WHITE

    def update(self, position):
        self.position = position
        self.size = pr.Rectangle(self.position.x, self.position.y, 50, 15)

    def draw(self):
        pr.draw_rectangle_rec(
            self.size,
            self.color
            )
            
