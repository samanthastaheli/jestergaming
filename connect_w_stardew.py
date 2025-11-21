import pyautogui
import keyboard
import pygetwindow as gw
from game_input import PressKey, ReleaseKey
import time

print("starting")
time.sleep(3)

input_types = ["up_right", "right", "down_right", "down_left", "left", "up_left"]
i=0

move_input = "none"
action_input = "none"

try:
    game_window = gw.getWindowsWithTitle('Stardew Valley')[0]
    game_window.activate()
    print("found window")
except IndexError:
    print("couldn't find it")
while True:
    if keyboard.is_pressed('esc'):
        print("stopped")
        break

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


    #Match camera output to input key

    move_input = input_types[i]
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
        case "1":
            action_key=0x31
        case "2":
            action_key=0x32
        case "3":
            action_key=0x33
        case "4":
            action_key=0x34
        case "5":
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

        

    move_key=0x00
    action_key=0x00


    i+=1
    i=i%6

    if(i==0):
        action_input="tool"
    else:
        action_input="none"