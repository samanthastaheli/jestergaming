import pyautogui
import keyboard
import pygetwindow as gw
from game_input import PressKey, ReleaseKey
import time
from pynput.mouse import Controller
mouse = Controller()

 ######## INPUT CODES #########
    # Left click = 0x01
    # Right click = 0x02
    # Escape = 0x1B
    # Tab = 0x09
    # W = 0x57
    # A = 0x41
    # S = 0x53
    # D = 0x44
    # F = 0x46
    # M = 0x4D
    # 0 = 0x30
    # 1 = 0x31
    # 2 = 0x32
    # 3 = 0x33
    # 4 = 0x34
    # 5 = 0x35
    # 6 = 0x36
    # 7 = 0x37
    # 8 = 0x38
    # 9 = 0x39

print("starting")

actions = { "tool":0x01, #click once
            "holdTool":0x01, #hold command
            "action":0x02, #click once
            "menu":0x1B, #switch to mouse input
            "closeMenu":0x01,
            "one":0x31, #click once
            "two":0x32, #click once
            "three":0x33, #click once
            "four":0x34, #click once
            "five":0x35, #click once
            "journal": 0x46, #switch to mouse input
            "map": 0x4D, #hold
            "toolbar":0x09,#click once
            "none":0x00,
            "":0x00
            }

movements = {   "up": [0x57,0x00],
                "down":[0x53,0x00],
                "left":[0x41,0x00],
                "right":[0x44,0x00],
                "up_right":[0x57,0x44],
                "down_right":[0x53,0x44],
                "up_left":[0x57,0x41],
                "down_left":[0x53,0x41],
                "none":[0x00,0x00],
                "":[0x00,0x00]
                }

move_input = "none"
action_input = "none"

def connect_to_window():
    try:
        game_window = gw.getWindowsWithTitle('Stardew Valley')[0]
        game_window.activate()
        print("found window")
    except IndexError:
        print("couldn't find it")

def control_game(move_input, action_input):
    move_key = 0x00
    move_key2 = 0x00
    action_key=0x00
    #Left half of screen = movement
    match move_input:
        case "up": #W
            move_key=0x57
        case "down": #S
            move_key=0x53
        case "left": #A
            move_key=0x41
        case "right": #D
            move_key=0x44
        case "up_right":
            move_key=0x57
            move_key2=0x44
        case "up_left":
            move_key=0x57
            move_key2=0x41
        case "down_right":
            move_key=0x53
            move_key2=0x44
        case "down_left":
            move_key=0x53
            move_key2=0x41
        case _:
            move_key=0x00
            move_key2=0x00
                
    #right half of the screen = actions
    match action_input:
        case "tool":
            action_key=0x01
        case "action":
            action_key=0x02
        case "menu":
            action_key=0x1B
        case "one":
            action_key=0x31
        case "two":
            action_key=0x32
        case "three":
            action_key=0x33
        case "four":
            action_key=0x34
        case "five":
            action_key=0x35
        case "journal":
            action_key=0x46
        case "map":
            action_key=0x4D
        case "toolbar":
            action_key=0x09
        case _:
            action_key=0x00

    if(move_key!=0x00):
        PressKey(move_key)
        if (move_key2!=0x00):
            PressKey(move_key2)
        time.sleep(.3)
        ReleaseKey(move_key)
        if (move_key2!=0x00):
            ReleaseKey(move_key2)

    if(action_key!=0x00):
        PressKey(action_key)
        time.sleep(.3)
        ReleaseKey(action_key)

def press_action(action_input):
    action_key=actions[action_input]
                
    if(action_key!=0x00):
        PressKey(action_key)

def release_action(action_input):
    action_key=actions[action_input]
                
    if(action_key!=0x00):
        ReleaseKey(action_key)

def press_movement(move_x, move_y):
    move_key1,_=movements[move_x]
    move_key2,_=movements[move_y]
                
    if(move_key1!=0x00):
        PressKey(move_key1)
    if(move_key2!=0x00):
        PressKey(move_key2)

def release_movement(move_x, move_y):
    move_key1,_=movements[move_x]
    move_key2,_=movements[move_y]
                
    if(move_key1!=0x00):
        ReleaseKey(move_key1)
    if(move_key2!=0x00):
        ReleaseKey(move_key2)


def move_mouse_old(x_offset, y_offset, sec):
    pyautogui.move(x_offset, y_offset)#, duration=sec, tween=pyautogui.easeOutQuad)

def move_mouse(dx, dy):
    # x, y = win32api.GetCursorPos()
    # win32api.SetCursorPos((x + dx, y + dy))
    mouse.move(dx, dy)