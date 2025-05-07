import pyray as pr
import json
import math
from tile import Tile
from player import Player
from input import Input
from ball import Ball

pr.init_window(640, 360, "breakout")
pr.set_target_fps(60)

###############
#  constants  #
###############
LEVEL = (0,)
TILE_COUNT = pr.Vector2(8, 6)
TILE_SIZE = pr.Vector2(pr.get_screen_width() // TILE_COUNT.x, 20)
PLAYER_SPEED = 5
BALL_SPEED = 3
###############
#   varables  #
###############
'''here 25 and 15 are offesets based on player width and height'''
player_position = pr.Vector2(pr.get_screen_width() // 2 - 25, pr.get_screen_height() - 20)
'''here 5 is the radius of the ball and 25 offset from rect start'''
ball_position = pr.Vector2(player_position.x + 25, player_position.y - 5)
ball_direction = -90
delta = pr.get_frame_time()
###############
#   objects   #
###############
player = Player(player_position)
ball = Ball(ball_position, ball_direction)

###############
#json loading #
###############
with open("params.json") as file:
    level_json = json.load(file)

LEVEL = level_json["level1"]

################
#game functions#
################
def show_map():
    for i in range(int(TILE_COUNT.x)):
        for j in range(int(TILE_COUNT.y)):
            if LEVEL[j][i] == "1":
                tile = Tile(i, j, TILE_SIZE)
                tile.draw()

def show_player():
    player.draw()

def show_ball():
    ball.draw()

def move_player():
    if Input.is_action_pressed("ui_left"):
        player_position.x += -1 * PLAYER_SPEED
    elif Input.is_action_pressed("ui_right"):
        player_position.x += 1 * PLAYER_SPEED
    player.update(player_position)

def move_ball():
    dir_rad = math.radians(ball_direction)
    ball_position.x += BALL_SPEED * math.cos(dir_rad)
    ball_position.y += BALL_SPEED * math.sin(dir_rad)
    ball.update(ball_position, ball_direction)

###############
#  game loop  #
###############
while not pr.window_should_close():
    pr.begin_drawing()
    pr.clear_background(pr.BLACK)
    move_player()
    move_ball()
    show_map()
    show_player()
    show_ball()
    pr.end_drawing()
pr.close_window()
