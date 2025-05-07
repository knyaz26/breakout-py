import pyray as pr

class Tile:
    def __init__(self, x, y, current_tile_size):
        self.x = x
        self.y = y
        self.tile_size = current_tile_size
        colors = [pr.RED, pr.ORANGE, pr.GREEN]
        self.color = colors[y//2]

    def draw(self):
         pr.draw_rectangle(
            int(self.x * self.tile_size.x),
            int(self.y * self.tile_size.y),
            int(self.tile_size.x - 4),
            int(self.tile_size.y - 4),
            self.color
            )

