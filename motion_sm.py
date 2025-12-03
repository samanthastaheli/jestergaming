from connect_w_stardew import press_movement, release_movement

CURRENT_STATE = "start"
CURRENT_X = "none"
CURRENT_Y = "none"
INDEX = 10

def call_motion_state(motion_x,motion_y):
    if CURRENT_STATE == "start":
        start_game()
    elif CURRENT_STATE == "move":
        move(motion_x,motion_y)
    else:
        no_movement(motion_x,motion_y)

def start_game():
    global CURRENT_STATE
    CURRENT_STATE = "no"
    no_movement("none","none")

def no_movement(motion_x,motion_y):
    global CURRENT_STATE, INDEX, CURRENT_X, CURRENT_Y
    if motion_x != "none" or motion_y != "none":
        press_movement(motion_x,motion_y)
        CURRENT_X = motion_x
        CURRENT_Y = motion_y
        CURRENT_STATE = "move"
        INDEX = 3
        # move(motion_x,motion_y)

def move(motion_x,motion_y):
    global CURRENT_STATE, INDEX
    if INDEX <= 0:
        release_movement(CURRENT_X,CURRENT_Y)
        CURRENT_STATE = "no"
        INDEX = 3
        # no_movement(motion_x,motion_y)
    else:
        INDEX = INDEX-1
        # move(motion_x,motion_y)