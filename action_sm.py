from connect_w_stardew import press_action, release_action

CURRENT_STATE = "init"
CURRENT_ACTION = "none"
CLICK_ACTION = "none"
MAP_QUEUE = []
TOOL_QUEUE = []
HOLD_ACTION = "none"
INDEX = 2
START_INDEX = 5
TOOL_INDEX = 1

def call_action_state(action, motion_x, motion_y):
    global MAP_QUEUE, TOOL_QUEUE

    TOOL_QUEUE.append(action)
    if len(TOOL_QUEUE) > 3:
        TOOL_QUEUE.pop(0)

    if CURRENT_STATE == "init":
        init()
    elif CURRENT_STATE == "click":
        click_once(action)
    elif CURRENT_STATE == "holdMap":
        MAP_QUEUE.append(action)
        if len(MAP_QUEUE) > 3:
            MAP_QUEUE.pop(0)
        holdMap(action)
    elif CURRENT_STATE == "holdTool":
        holdTool(action)
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
    global CURRENT_STATE, INDEX, CURRENT_ACTION, HOLD_ACTION,MAP_QUEUE,TOOL_QUEUE
    if action != "none":
        CURRENT_ACTION = action
        HOLD_ACTION = action
    
        INDEX = 2
        if action == "map":
            press_action(HOLD_ACTION)
            CURRENT_STATE = "holdMap"
        if action == "holdTool":
            press_action(HOLD_ACTION)
            CURRENT_STATE = "holdTool"
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

def holdMap(action):
    global CURRENT_STATE, MAP_QUEUE
 
    print("Hold Action: ", HOLD_ACTION)
    if HOLD_ACTION not in MAP_QUEUE:
        print("left hold")
        press_action(HOLD_ACTION)
        CURRENT_STATE = "release"
    else:
        release_action(HOLD_ACTION)
        print("still hold")

def holdTool(action):
    global CURRENT_STATE, TOOL_INDEX,TOOL_QUEUE

    print("Hold Action: ", HOLD_ACTION)
    if TOOL_INDEX % 2 == 0:
        release_action(HOLD_ACTION)
    else:
        press_action(HOLD_ACTION)

    TOOL_INDEX+=1 

    if HOLD_ACTION not in TOOL_QUEUE:
        print("left hold")
        CURRENT_STATE = "release"

def mouse_control(action):
    global CURRENT_STATE
    press_action(CURRENT_ACTION)
    CURRENT_STATE = "release"

def release(action):
    global CURRENT_STATE, CURRENT_ACTION, INDEX
    release_action(CURRENT_ACTION)
    release_action(HOLD_ACTION)
    CURRENT_STATE = "no"