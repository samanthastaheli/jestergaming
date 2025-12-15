import pyautogui
import keyboard
import pygetwindow as gw
from game_input import PressKey, ReleaseKey
import time
from pynput.mouse import Controller
mouse = Controller()

MOUSE_SPEED = .7

 ######## INPUT CODES #########
    # Left click = 0x01
    # Right click = 0x02
    # Escape = 0x1B
    # Tab = 0x09
    # Shift = 0x10
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

#print("starting")
SHIFT_KEY = 0x10

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

movements = {   "up": 0x57,
                "down":0x53,
                "left":0x41,
                "right":0x44,
                "none":0x00,
                "":0x00
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

def press_action(action_input):
    action_key=actions[action_input]
                
    if(action_key!=0x00):
        PressKey(action_key)

def release_action(action_input):
    action_key=actions[action_input]
                
    if(action_key!=0x00):
        ReleaseKey(action_key)

def press_movement(move_x, move_y, bIsShift):
    move_key1=movements[move_x]
    move_key2=movements[move_y]
                
    if(move_key1!=0x00):
        PressKey(move_key1)
    if(move_key2!=0x00):
        PressKey(move_key2)
    if bIsShift:
        PressKey(SHIFT_KEY)

def release_movement(move_x, move_y, bIsShift):
    move_key1=movements[move_x]
    move_key2=movements[move_y]
                
    if(move_key1!=0x00):
        ReleaseKey(move_key1)
    if(move_key2!=0x00):
        ReleaseKey(move_key2)
    if bIsShift:
        ReleaseKey(SHIFT_KEY)

def move_mouse(dx, dy):
    # x, y = win32api.GetCursorPos()
    # win32api.SetCursorPos((x + dx, y + dy))
    mouse.move(dx*MOUSE_SPEED, dy*MOUSE_SPEED)