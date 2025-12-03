from connect_w_stardew import press_action, release_action

CURRENT_STATE = "init"
CURRENT_ACTION = "none"
CLICK_ACTION = "none"
INDEX = 2
START_INDEX = 5

def call_action_state(action):
    if CURRENT_STATE == "init":
        init()
    elif CURRENT_STATE == "click":
        click_once(action)
    elif CURRENT_STATE == "hold":
        hold(action)
    elif CURRENT_STATE == "mouse":
        mouse_control(action)
    elif CURRENT_STATE == "release":
        release(action)
    else:
        no_action(action)

def init():
    global CURRENT_STATE, START_INDEX
    if START_INDEX <= 0:
        CURRENT_STATE = "no"
    START_INDEX -= 1
    # no_movement("none","none")

def no_action(action):
    global CURRENT_STATE, INDEX, CURRENT_ACTION
    if action != "none":
        CURRENT_ACTION = action
        INDEX = 2
        if action in ["holdTool", "map"]:
            press_action(CURRENT_ACTION)
            CURRENT_STATE = "hold"
        elif action in ["menu", "journal"]:
            CURRENT_STATE = "mouse"
        else:
            if CURRENT_ACTION != CLICK_ACTION:
                CURRENT_STATE = "click"

def click_once(action):
    global CURRENT_STATE, CLICK_ACTION
    press_action(CURRENT_ACTION)
    CURRENT_STATE = "release"
    CLICK_ACTION = CURRENT_ACTION


def hold(action):
    global CURRENT_STATE
    if action != CURRENT_ACTION:
        press_action(CURRENT_ACTION)
        CURRENT_STATE = "release"
    else:
        release_action(CURRENT_ACTION)

def mouse_control(action):
    global CURRENT_STATE
    press_action(CURRENT_ACTION)
    CURRENT_STATE = "release"

def release(action):
    global CURRENT_STATE, CURRENT_ACTION, INDEX
    release_action(CURRENT_ACTION)
    CURRENT_STATE = "no"