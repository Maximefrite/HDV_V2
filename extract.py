import time
import pyautogui
from PIL import ImageGrab
import os
from datetime import datetime

def is_pixel_color_255_153_17(y):
    return pyautogui.pixel(658, y) == (255, 153, 17)

def take_screenshot(xmin, ymin, xmax, ymax, file_path):
    width = xmax - xmin
    height = ymax - ymin
    img = ImageGrab.grab(bbox=(xmin, ymin, xmin + width, ymin + height))
    img.save(file_path)

def screen_nom_ressource(i):
    xmin, ymin, xmax, ymax = 1151, 146, 1753, 184
    file_path = f'/home/human1/HDV_V2/Screens/screenshot_r{i}.png'
    take_screenshot(xmin, ymin, xmax, ymax, file_path)

def screen_prix_x1(i):
    xmin, ymin, xmax, ymax = 1190, 560, 1346, 594
    file_path = f'/home/human1/HDV_V2/Screens/screenshot_r{i}_x1.png'
    take_screenshot(xmin, ymin, xmax, ymax, file_path)

def screen_prix_x10(i):
    xmin, ymin, xmax, ymax = 1351, 560, 1507, 594
    file_path = f'/home/human1/HDV_V2/Screens/screenshot_r{i}_x10.png'
    take_screenshot(xmin, ymin, xmax, ymax, file_path)

def screen_prix_x100(i):
    xmin, ymin, xmax, ymax = 1512, 560, 1668, 594
    file_path = f'/home/human1/HDV_V2/Screens/screenshot_r{i}_x100.png'
    take_screenshot(xmin, ymin, xmax, ymax, file_path)

t1 = 0.2
t2 = 0.1

y_pos = [295, 331, 368, 406, 445, 483, 518, 553, 593, 628, 669, 700]
y_or = [280, 317, 353, 389, 426, 464, 500, 537, 574, 611, 650, 685]

# 1) Update extract to accept start_row (default 0)
def extract(start_i=1, start_row=0):
    i = start_i
    rows = y_pos[start_row:]  # start from the requested position
    for y in rows:
        time.sleep(t2)
        pyautogui.moveTo(1000, y)
        time.sleep(t2)
        pyautogui.click()
        time.sleep(t1)
        screen_nom_ressource(i)
        screen_prix_x1(i)
        screen_prix_x10(i)
        screen_prix_x100(i)
        i += 1
    return i  # next filename index

# 2) In more(), pass start_row when a match is found
def more():
    idx = 1  # start numbering at r1
    for loop_idx in range(5):
        if loop_idx >= 1:
            found_index = None
            for j, y in enumerate(y_or):
                if is_pixel_color_255_153_17(y):
                    found_index = j
                    print(f"[INFO] Orange pixel detected at position {j} (y={y})")
                    break

            if found_index is not None:
                start_row = found_index + 1
                print(f"[INFO] Starting extract() from y_pos index {start_row}")
                if start_row >= len(y_pos):
                    # nothing left in this page�just do the scroll behavior
                    pyautogui.moveTo(1090, 321)
                    time.sleep(t2)
                    pyautogui.scroll(-4)
                    time.sleep(t2)
                    continue
                idx = extract(idx, start_row=start_row)
            else:
                idx = extract(idx)
        else:
            idx = extract(idx)

        # scroll after each batch
        pyautogui.moveTo(1090, 321)
        time.sleep(t2)
        pyautogui.scroll(-4)
        time.sleep(t2)

if __name__ == "__main__":
    # Clear screenshots directory
    screenshots_dir = '/home/human1/HDV_V2/Screens'
    for filename in os.listdir(screenshots_dir):
        file_path = os.path.join(screenshots_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error: {e}")
    more()
