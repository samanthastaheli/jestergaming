from connect_w_stardew import press_movement, release_movement, move_mouse

CURRENT_STATE = "init"
CURRENT_X = "none"
CURRENT_Y = "none"
INDEX = 2
START_INDEX = 5
MOUSE_MOVE_SPEED = 7

def call_motion_state(motion, motion_x,motion_y):
    if CURRENT_STATE == "init":
        init()
    elif CURRENT_STATE == "move":
        move(motion_x,motion_y)
    elif CURRENT_STATE == "release":
        release_move(motion_x, motion_y)
    elif CURRENT_STATE == "one":
        mouse_control(motion, motion_x,motion_y)
    else:
        no_movement(motion,motion_x,motion_y)

def init():
    global CURRENT_STATE, START_INDEX
    if START_INDEX <= 0:
        CURRENT_STATE = "no"
    START_INDEX -= 1

def no_movement(motion, motion_x,motion_y):
    global CURRENT_STATE, INDEX, CURRENT_X, CURRENT_Y
    if motion=="move":
        CURRENT_X = motion_x
        CURRENT_Y = motion_y
        CURRENT_STATE = "move"
        INDEX = 2
    if motion=="one":
        CURRENT_STATE = "one"

def move(motion_x,motion_y):
    global CURRENT_STATE, INDEX
    press_movement(motion_x,motion_y)
    if INDEX <= 0:
        if(motion_x != CURRENT_X or motion_y != CURRENT_Y):
            CURRENT_STATE = "release"
    else:
        INDEX = INDEX-1

def mouse_control(motion, motion_x, motion_y):
    global CURRENT_STATE
    move = False
    x_offset = 0
    y_offset = 0
    if motion_x == "left":
        x_offset = -MOUSE_MOVE_SPEED
        move = True
    elif motion_x == "right":
        x_offset = MOUSE_MOVE_SPEED
        move = True
    if motion_y == "down":
        y_offset = MOUSE_MOVE_SPEED
        move = True
    elif motion_y == "up":
        y_offset = -MOUSE_MOVE_SPEED
        move = True

    if move == True:
        move_mouse(x_offset, y_offset)

    if motion != "one":
        CURRENT_STATE = "no"

def release_move(motion_x,motion_y):
    global CURRENT_STATE, CURRENT_X, CURRENT_Y, INDEX
    release_movement(CURRENT_X,CURRENT_Y)

    if(motion_x == "none" and motion_y == "none"):
        CURRENT_STATE = "no"
    else:
        CURRENT_STATE = "move"
        INDEX = 2
        CURRENT_X = motion_x
        CURRENT_Y = motion_y