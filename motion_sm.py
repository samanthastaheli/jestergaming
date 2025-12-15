from connect_w_stardew import press_movement, release_movement, move_mouse

CURRENT_STATE = "init"
CURRENT_X = "none"
CURRENT_Y = "none"
INDEX = 1
START_INDEX = 5
MOUSE_MOVE_SPEED = 7
SHIFT = False

def call_motion_state(motion, motion_x,motion_y):
    if CURRENT_STATE == "init":
        init()
    elif CURRENT_STATE == "move":
        move(motion,motion_x,motion_y)
    elif CURRENT_STATE == "release":
        release_move(motion, motion_x, motion_y)
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
    global CURRENT_STATE, INDEX, CURRENT_X, CURRENT_Y,SHIFT
    if motion =="move":
        CURRENT_X = motion_x
        CURRENT_Y = motion_y
        CURRENT_STATE = "move"
        INDEX = 1
    elif motion=="one":
        CURRENT_STATE = "one"
    # if motion == "run":
    #     SHIFT = not SHIFT
    # else:
    #     CURRENT_STATE = "no"

def move(motion,motion_x,motion_y):
    global CURRENT_STATE, INDEX, SHIFT
    # SHIFT = True
    # if motion=="run":
    #     SHIFT=False
    press_movement(motion_x,motion_y,SHIFT)
    if INDEX <= 0:
        if(motion_x != CURRENT_X or motion_y != CURRENT_Y):
        # if(motion!="move"):
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

def release_move(motion, motion_x,motion_y):
    global CURRENT_STATE, CURRENT_X, CURRENT_Y, INDEX
    release_movement(CURRENT_X,CURRENT_Y, SHIFT)

    if(motion_x == "none" and motion_y == "none"):
        CURRENT_STATE = "no"
    else:
        CURRENT_STATE = "move"
        INDEX = 1
        CURRENT_X = motion_x
        CURRENT_Y = motion_y