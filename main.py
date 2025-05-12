import pyray as pr
import json
from tile import Tile
from player import Player
from input import Input
from ball import Ball
from event_manager import event_handler

# ──────────────────────────────
#         Configuration
# ──────────────────────────────
LEVEL_DATA_PATH = "params.json"
LEVEL_KEY = "level1"

DEFAULT_TILE_COLUMNS = 8
DEFAULT_TILE_HEIGHT = 20
TILE_SIZE = pr.Vector2(pr.get_screen_width() // DEFAULT_TILE_COLUMNS, DEFAULT_TILE_HEIGHT)

PLAYER_SPEED = 5
BALL_SPEED = 3
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 15
BALL_RADIUS = 5

STATE_IDLE = "idle"
STATE_RUNNING = "running"

# ──────────────────────────────
#            Game
# ──────────────────────────────
class Game:
    def __init__(self):
        self.current_state = STATE_IDLE
        self.level_data = []
        self.tile_size_for_level = TILE_SIZE
        
        initial_player_pos_x = pr.get_screen_width() // 2 - (PLAYER_WIDTH // 2)
        initial_player_pos_y = pr.get_screen_height() - PLAYER_HEIGHT - 5
        
        self.player = Player(
            pr.Vector2(initial_player_pos_x, initial_player_pos_y),
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
            PLAYER_SPEED
        )

        self.ball = Ball(
            pr.Vector2(0, 0),
            -90.0,
            BALL_RADIUS,
            BALL_SPEED
        )
        
        self._setup_event_handlers()
        self.reset_elements()

    def _setup_event_handlers(self):
        event_handler.subscribe("ball_hit_tile", self._on_ball_hit_tile)
        event_handler.subscribe("ball_hit_player", self._on_ball_hit_player)

    # ────────────────
    # Load/reset state
    # ────────────────
    def reset_elements(self):
        with open(LEVEL_DATA_PATH) as file:
            level_json = json.load(file)
        self.level_data = level_json.get(LEVEL_KEY, [])

        if self.level_data and len(self.level_data) > 0 and len(self.level_data[0]) > 0:
            num_cols_in_level = len(self.level_data[0])
            self.tile_size_for_level = pr.Vector2(
                pr.get_screen_width() // num_cols_in_level,
                DEFAULT_TILE_HEIGHT
            )
        else:
            self.level_data = []
            self.tile_size_for_level = TILE_SIZE 

        self.player.reset()
        self.ball.reset(self.player.size)
        self.current_state = STATE_IDLE

    # ────────────────
    # Event responses
    # ────────────────
    def _on_ball_hit_tile(self, grid_x, grid_y):
        if 0 <= grid_y < len(self.level_data) and 0 <= grid_x < len(self.level_data[grid_y]):
            if self.level_data[grid_y][grid_x] == "1":
                row_list = list(self.level_data[grid_y])
                row_list[grid_x] = "0"
                self.level_data[grid_y] = "".join(row_list)
                self.ball.direction = -self.ball.direction

    def _on_ball_hit_player(self):
        paddle_center_x = self.player.position.x + (self.player.width / 2)
        hit_offset_x = self.ball.position.x - paddle_center_x
        normalized_hit_offset = hit_offset_x / (self.player.width / 2)
        normalized_hit_offset = max(-1, min(1, normalized_hit_offset))
            
        max_reflection_angle_offset = 60 
        new_angle_degrees = -90 + (normalized_hit_offset * max_reflection_angle_offset)
        self.ball.direction = new_angle_degrees
        
        if self.ball.position.y + self.ball.radius > self.player.position.y:
           self.ball.position.y = self.player.position.y - self.ball.radius - 0.1

    # ──────────────────────────
    # Input + game logic update
    # ──────────────────────────
    def _handle_input(self):
        if self.current_state == STATE_IDLE:
            if Input.is_action_pressed("ui_accept"):
                self.current_state = STATE_RUNNING

    def _update_game_world(self):
        if self.current_state == STATE_RUNNING:
            self.player.move(pr.get_screen_width())
            self.ball.move()
            
            wall_collision_result = self.ball.check_wall_collision(pr.get_screen_width(), pr.get_screen_height())
            if wall_collision_result == "bottom_wall_hit":
                self.reset_elements() 
                return 

            collided_this_frame = False
            if self.level_data and len(self.level_data) > 0:
                num_rows = len(self.level_data)
                num_cols = len(self.level_data[0]) 

                for j in range(num_rows): 
                    if collided_this_frame:
                        break
                    for i in range(num_cols): 
                        if i < len(self.level_data[j]): 
                            if self.level_data[j][i] == "1": 
                                tile_rect = pr.Rectangle(
                                    i * self.tile_size_for_level.x, 
                                    j * self.tile_size_for_level.y,
                                    self.tile_size_for_level.x - 4,
                                    self.tile_size_for_level.y - 4
                                )
                                if pr.check_collision_circle_rec(self.ball.position, self.ball.radius, tile_rect):
                                    event_handler.emit("ball_hit_tile", i, j)
                                    collided_this_frame = True
                                    break 
                        if collided_this_frame: 
                            break
            
            if not collided_this_frame:
                if pr.check_collision_circle_rec(self.ball.position, self.ball.radius, self.player.size):
                    event_handler.emit("ball_hit_player")

    def update(self):
        self._handle_input()
        self._update_game_world()

    # ──────────────────────
    # Drawing game elements
    # ──────────────────────
    def _draw_level(self):
        if not self.level_data or len(self.level_data) == 0:
            return
        
        num_rows = len(self.level_data)
        num_cols = len(self.level_data[0]) if num_rows > 0 else 0

        for j in range(num_rows): 
            for i in range(num_cols): 
                if i < len(self.level_data[j]): 
                    if self.level_data[j][i] == "1":
                        tile = Tile(i, j, self.tile_size_for_level)
                        tile.draw()
    
    def _draw_ui(self):
        if self.current_state == STATE_IDLE:
            text = "Press Enter or Space to Start"
            text_size = 20
            text_width = pr.measure_text(text, text_size)
            pr.draw_text(text, pr.get_screen_width() // 2 - text_width // 2, 
                          pr.get_screen_height() // 2 - text_size // 2, 
                          text_size, pr.RAYWHITE)

    def draw(self):
        pr.begin_drawing()
        pr.clear_background(pr.BLACK)
        
        self._draw_level()
        self.player.draw()
        self.ball.draw()
        self._draw_ui()
        
        pr.end_drawing()

# ──────────────────────────────
#       Game Entry Point
# ──────────────────────────────
pr.init_window(640, 360, "breakout")
pr.set_target_fps(60)

game = Game()

while not pr.window_should_close():
    game.update()
    game.draw()
    
pr.close_window()
