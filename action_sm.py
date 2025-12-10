from connect_w_stardew import press_action, release_action, move_mouse
from collections import Counter

CURRENT_STATE = "init"
CURRENT_ACTION = "none"
PREVIOUS_CLICK = "none"
CLICK_ACTION = "none"
MAP_QUEUE = []
TOOL_QUEUE = []
HOLD_ACTION = "none"
INDEX = 2
START_INDEX = 5
TOOL_INDEX = 1
FIRST_HOLD = 1
DEBOUNCE_CLICK = []
RELEASE_NEXT = False
RELEASE_MENU = False
MOUSE_MOVE_SPEED = 7
ACTION_TO_RELEASE = "none"


def call_action_state(action, motion_x, motion_y):
    global MAP_QUEUE, TOOL_QUEUE, DEBOUNCE_CLICK

    DEBOUNCE_CLICK.append(action)
    if len(DEBOUNCE_CLICK) > 4:
        DEBOUNCE_CLICK.pop(0)

    # action_to_call = DEBOUNCE
    click_action = "none"
    most_common_action, count = Counter(DEBOUNCE_CLICK).most_common(1)[0]
    if count > 1:
        click_action = most_common_action

    # print(DEBOUNCE_CLICK)

    TOOL_QUEUE.append(click_action)
    if len(TOOL_QUEUE) > 3:
        TOOL_QUEUE.pop(0)

    MAP_QUEUE.append(click_action)
    if len(MAP_QUEUE) > 5:
        MAP_QUEUE.pop(0)


    if CURRENT_STATE == "init":
        init()
    elif CURRENT_STATE == "click":
        print("went to click with ", click_action)
        click_once(click_action)
    elif CURRENT_STATE == "holdMap":
        holdMap(action)
    elif CURRENT_STATE == "holdTool":
        holdTool(action)
    elif CURRENT_STATE == "mouse":
        mouse_control(click_action, motion_x, motion_y)
    elif CURRENT_STATE == "release":
        release(action)
    else:
        no_action(click_action)

def init():
    global CURRENT_STATE, START_INDEX
    if START_INDEX <= 0:
        CURRENT_STATE = "no"
    START_INDEX -= 1

def no_action(action):
    global CURRENT_STATE, ACTION_TO_RELEASE,INDEX, CURRENT_ACTION, HOLD_ACTION,MAP_QUEUE,TOOL_QUEUE,START_INDEX, TOOL_INDEX, FIRST_HOLD, RELEASE_NEXT, RELEASE_MENU
    
    # print("NO ACTION STATE ---------------------------------")
    if action not in ["none", ""]:
        CURRENT_ACTION = action
    
        INDEX = 2
        if action == "map":
            HOLD_ACTION = action
            press_action(HOLD_ACTION)
            release_action(HOLD_ACTION)
            print("pressed and released map")
            CURRENT_STATE = "holdMap"
        if action == "holdTool":
            HOLD_ACTION = action
            press_action(HOLD_ACTION)
            print("pressed holdTool: ",HOLD_ACTION)
            CURRENT_STATE = "holdTool"
        elif action == "menu":
            HOLD_ACTION = action
            press_action(CURRENT_ACTION)
            print("pressed menu")
            # release_action(HOLD_ACTION)
            CURRENT_STATE = "mouse"
        elif action == "journal":
            HOLD_ACTION = action
            press_action(HOLD_ACTION)
            print("pressed journal")
            # release_action(HOLD_ACTION)
            CURRENT_STATE = "mouse"
        elif action == "closeMenu":
            return
        # elif action in ["closeMenu", "map", "menu","journal"]:
        #     #nothing should happen with close menu unless you're using the menu
        #     return
        else:
            if CURRENT_ACTION != PREVIOUS_CLICK:
                CURRENT_STATE = "click"

    else:
        INDEX = 2
        START_INDEX = 5
        TOOL_INDEX = 1
        FIRST_HOLD = 1
        RELEASE_NEXT = False
        RELEASE_MENU = False
        ACTION_TO_RELEASE = "none"
        release_action("map")

def click_once(action):
    global CURRENT_STATE, PREVIOUS_CLICK,ACTION_TO_RELEASE

    print("CLICK ONCE STATE ---------------------------------")
    press_action(CURRENT_ACTION)
    ACTION_TO_RELEASE = CURRENT_ACTION
    CURRENT_STATE = "release"
    PREVIOUS_CLICK = CURRENT_ACTION

def holdMap(action):
    global CURRENT_STATE, MAP_QUEUE, FIRST_HOLD,ACTION_TO_RELEASE
    
    print("HOLD MAP STATE ---------------------------------")
    # #print("Hold Action: ", HOLD_ACTION)
    # if FIRST_HOLD == 1:
    #     FIRST_HOLD -= 1
    #     release_action(HOLD_ACTION)
    #     return
    #print(MAP_QUEUE)
    if HOLD_ACTION not in MAP_QUEUE:
        #print("left hold----------------------------------------------------------------------")
        press_action(HOLD_ACTION)
        print("in holdMap, pressed: ", HOLD_ACTION)
        ACTION_TO_RELEASE = HOLD_ACTION
        CURRENT_STATE = "release"
    # else:
    #     release_action(HOLD_ACTION)
    #     # #print("still hold")

def holdTool(action):
    global CURRENT_STATE, TOOL_INDEX,TOOL_QUEUE,ACTION_TO_RELEASE

    print("HOLDTOOL STATE ---------------------------------")
    # #print("Hold Action: ", HOLD_ACTION)
    if TOOL_INDEX % 2 == 0:
        release_action(HOLD_ACTION)
    else:
        press_action(HOLD_ACTION)

    TOOL_INDEX+=1 

    if HOLD_ACTION not in TOOL_QUEUE:
        # #print("left hold")
        ACTION_TO_RELEASE = HOLD_ACTION
        CURRENT_STATE = "release"

def mouse_control(action, motion_x, motion_y):
    global CURRENT_STATE, RELEASE_NEXT, CLICK_ACTION, RELEASE_MENU, ACTION_TO_RELEASE
    # press_action(HOLD_ACTION)
    print("MOUSE STATE ---------------------------------")

    if RELEASE_MENU == True:
        press_action(HOLD_ACTION)
        print("in mouse, pressed: ",HOLD_ACTION)
        ACTION_TO_RELEASE = HOLD_ACTION
        CURRENT_STATE = "release"
        RELEASE_MENU = False
        RELEASE_NEXT = False
        return
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

    # control mouse click while in menu or journal
    if RELEASE_NEXT == True:
        release_action(CLICK_ACTION)
        print("in mouse control, released: ",CLICK_ACTION)
        RELEASE_NEXT = False
    elif action == "tool" and action != CLICK_ACTION:
        CLICK_ACTION = "tool"
        press_action(CLICK_ACTION)
        print("in mouse control, pressed: ",CLICK_ACTION)
        RELEASE_NEXT = True

    if action != "tool":
        CLICK_ACTION = "none"


    if action == "closeMenu":
        #print("here")
        #print(HOLD_ACTION)
        # press_action(HOLD_ACTION)
        release_action(HOLD_ACTION)
        print("in mouse, released: ",HOLD_ACTION)
        # press_action(HOLD_ACTION)
        RELEASE_MENU = True


def release(action):
    global CURRENT_STATE, CURRENT_ACTION, INDEX, FIRST_HOLD, RELEASE_MENU

    print("RELEASE STATE ---------------------------------")
    # if CLICK_ACTION != "none":
    #     print("releasing click action: ", CLICK_ACTION)
    #     release_action(CLICK_ACTION)
    # elif CURRENT_ACTION == HOLD_ACTION:
    #     print("releasing current action: ", CURRENT_ACTION)
    #     release_action(CURRENT_ACTION)
    # else:
    #     print("releasing current action: ", CURRENT_ACTION)
    #     print("releasing hold action: ",HOLD_ACTION)
    #     release_action(HOLD_ACTION)
    #     release_action(CURRENT_ACTION)


    print("in release, releasing action: ", ACTION_TO_RELEASE)
    release_action(ACTION_TO_RELEASE)
    CURRENT_STATE = "no"
    FIRST_HOLD = 1
    RELEASE_MENU = False