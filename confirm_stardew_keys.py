import pyautogui
import keyboard
import pygetwindow as gw
from jestergaming.game_input import PressKey, ReleaseKey
import time

print("starting")
time.sleep(3)

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
    # 9 = 0x395

   
    print("W")
    PressKey(0x57)
    time.sleep(.3)
    ReleaseKey(0x57)

    time.sleep(2)

    print("S")  
    PressKey(0x53)
    time.sleep(.3)
    ReleaseKey(0x53)
    
    time.sleep(2)

# case "left": #A
    print("A")
    PressKey(0x41)
    time.sleep(.3)
    ReleaseKey(0x41)
    
    time.sleep(2)

# case "right": #D
    print("D")
    PressKey(0x44)
    time.sleep(.3)
    ReleaseKey(0x44)
    
    time.sleep(2)

# case "tool":
    print("Tool")
    PressKey(0x01)
    time.sleep(.3)
    ReleaseKey(0x01)
    
    time.sleep(2)

    
# case "action":
    print("action")
    PressKey(0x02)
    time.sleep(.3)
    ReleaseKey(0x02)
    
    time.sleep(2)

# case "menu":
    print("menu")
    PressKey(0x1B)
    time.sleep(.3)
    ReleaseKey(0x1B)
    time.sleep(.3)
    PressKey(0x1B)
    time.sleep(.3)
    ReleaseKey(0x1B)
    
    time.sleep(2)

# case "F":
    print("journal")
    PressKey(0x46)
    time.sleep(.3)
    ReleaseKey(0x46)
    time.sleep(.3)
    PressKey(0x46)
    time.sleep(.3)
    ReleaseKey(0x46)
    
    time.sleep(2)

# case "m":
    print("map")
    PressKey(0x4D)
    time.sleep(.3)
    ReleaseKey(0x4D)
    time.sleep(.3)
    PressKey(0x4D)
    time.sleep(.3)
    ReleaseKey(0x4D)
    
    time.sleep(2)

# case "tab":
    print("toolbar")
    PressKey(0x09)
    time.sleep(.3)
    ReleaseKey(0x09)
    
    time.sleep(2)

# case "1":
    print("1")
    PressKey(0x31)
    time.sleep(.3)
    ReleaseKey(0x31)
    
    time.sleep(2)

# case "2":
    print("2")
    PressKey(0x32)
    time.sleep(.3)
    ReleaseKey(0x32)
    
    time.sleep(2)

# case "3":
    print("3")
    PressKey(0x33)
    time.sleep(.3)
    ReleaseKey(0x33)
    
    time.sleep(2)

# case "4":
    print("4")
    PressKey(0x34)
    time.sleep(.3)
    ReleaseKey(0x34)
    
    time.sleep(2)

# case "5":
    print("5")
    PressKey(0x35)
    time.sleep(.3)
    ReleaseKey(0x35)
    
    time.sleep(2)



    # PressKey(0x46)#pyautogui.press('f')
    # print("pressed f")
    # time.sleep(3)
    # ReleaseKey(0x46)
    
    # PressKey(0x01)#pyautogui.click()  
    # print("left click")
    # time.sleep(3)
    # ReleaseKey(0x01)