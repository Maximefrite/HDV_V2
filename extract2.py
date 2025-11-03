import time
import pyautogui
from PIL import ImageGrab
import os
from datetime import datetime
from deplacement import (
    zapi_milice_to_hdv, go_to_hdv_alchimistes, go_to_hdv_bijoutiers,
    go_to_hdv_bouchers, go_to_hdv_boulangers, go_to_hdv_bricoleurs,
    go_to_hdv_bucherons, go_to_hdv_cordonniers, go_to_hdv_documents,
    go_to_hdv_forgerons, go_to_hdv_mineurs, go_to_hdv_paysans,
    go_to_hdv_pecheurs, go_to_hdv_ressources, go_to_hdv_runes,
    go_to_hdv_sculpteurs, go_to_hdv_tailleurs, take_screenshot
)

t1 = 0.1
t2 = 0.2
t5 = 0.5
t10 = 1.0
t20 = 2.0

def is_need_to_scrol():
    # FIX: use == instead of assignment
    return pyautogui.pixel(1092, 302) == (81, 74, 60)

def is_end_of_scrol():
    # FIX: use == instead of assignment
    return pyautogui.pixel(1089, 692) == (81, 74, 60)

def is_pixel_color_orange(y):
    return pyautogui.pixel(658, y) == (255, 153, 17)

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

y_pos = [295, 331, 368, 406, 445, 483, 518, 553, 593, 628, 669, 700]
y_or  = [280, 317, 353, 389, 426, 464, 500, 537, 574, 611, 650, 685]

def extract(start_i=1, start_row=0):
    i = start_i
    rows = y_pos[start_row:]  # start from the requested position
    for y in rows:
        time.sleep(t1)
        pyautogui.moveTo(1000, y)
        time.sleep(t1)
        pyautogui.click()
        time.sleep(t2)
        screen_nom_ressource(i)
        screen_prix_x1(i)
        screen_prix_x10(i)
        screen_prix_x100(i)
        i += 1
    return i  # next filename index

def extract_until_scrol_down():
    """
    Loop and extract until is_end_of_scrol() is True.
    First page: extract everything.
    Next pages: try to resume after the highlighted (orange) row if any; otherwise extract all visible rows.
    """
    idx = 1  # start numbering at r1
    first_page = True

    while True:
        if first_page:
            idx = extract(idx)
            first_page = False
        else:
            # Try to find the last "selected" (orange) line and continue after it
            found_index = None
            for j, y in enumerate(y_or):
                if is_pixel_color_orange(y):
                    found_index = j
                    break

            if found_index is not None:
                start_row = found_index + 1
                if start_row < len(y_pos):
                    idx = extract(idx, start_row=start_row)
                # else: nothing left on this page, just scroll
            else:
                # No orange selection: extract the whole page
                idx = extract(idx)

        # If we've reached the end, stop looping (no further scroll)
        if is_end_of_scrol():
            break

        # Scroll for the next batch
        pyautogui.moveTo(1090, 321)
        time.sleep(t1)
        pyautogui.scroll(-4)
        time.sleep(t1)

def run_once_or_full():
    """
    If no scrolling is needed, just extract once from the first row.
    Otherwise, run the scrolling extractor until the end.
    """
    if not is_need_to_scrol():
        extract(start_i=1, start_row=0)
    else:
        extract_until_scrol_down()

if __name__ == "__main__":
    screenshots_dir = '/home/human1/HDV_V2/Screens'
    for filename in os.listdir(screenshots_dir):
        file_path = os.path.join(screenshots_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error: {e}")

    # Decide strategy based on need to scroll
    run_once_or_full()
