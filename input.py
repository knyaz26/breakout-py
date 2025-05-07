import pyray as pr

class Input:
    action_key_map = {
        "ui_left": [pr.KEY_LEFT, pr.KEY_A],
        "ui_right": [pr.KEY_RIGHT, pr.KEY_D],
        "ui_accept": [pr.KEY_ENTER, pr.KEY_SPACE]
    }


    @staticmethod
    def is_action_pressed(action: str) -> bool:
        if action not in Input.action_key_map:
            return False
        for key in Input.action_key_map[action]:
            if pr.is_key_down(key):
                return True
        return False
