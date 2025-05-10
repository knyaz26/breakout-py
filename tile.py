import pyray as pr

class Tile:
    _next_id = 0
    
    def __init__(self, x, y, current_tile_size):
        self.x = x
        self.y = y
        self.tile_size = current_tile_size
        colors = [pr.RED, pr.ORANGE, pr.GREEN]
        self.color = colors[y // 2]
        
        self.id = Tile._next_id
        Tile._next_id += 1

        self.rect = pr.Rectangle(
            self.x * self.tile_size.x,
            self.y * self.tile_size.y,
            self.tile_size.x - 4,
            self.tile_size.y - 4
        )

    def draw(self):
        pr.draw_rectangle_rec(self.rect, self.color)
