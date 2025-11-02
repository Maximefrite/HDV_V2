import time
import pyautogui
from PIL import ImageGrab
import os
from datetime import datetime

t1 = 0.1
t2 = 0.2
t5 = 0.5
t10 = 1.0
t20 = 2.0

def zapi_milice_to_hdv():
    # TP milice brak
    pyautogui.moveTo(1472, 968)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t5)
    pyautogui.press('q')
    time.sleep(t20)
    # Click zapi
    pyautogui.moveTo(1573, 208)
    time.sleep(t5)
    pyautogui.rightClick()
    time.sleep(t20)
    # Click fenetre hdv
    pyautogui.moveTo(1055, 195)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)

def go_to_hdv_alchimistes():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 274)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1101, 394)
    time.sleep(t5)
    pyautogui.rightClick()
    time.sleep(t20)
    pyautogui.press('esc')
 
def go_to_hdv_bijoutiers():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 368)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1367, 416)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_bouchers():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 411)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1058, 665)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_boulangers():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 458)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1246, 453)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_bricoleurs():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 506)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(985, 144)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_bucherons():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 550)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1438, 706)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_cordonniers():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 597)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(948, 198)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_documents():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 643)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1101, 357)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_forgerons():
    zapi_milice_to_hdv()
    pyautogui.moveTo(1118, 689)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(986, 453)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_mineurs():
    zapi_milice_to_hdv()
    pyautogui.scroll(-4)
    time.sleep(t5)
    pyautogui.moveTo(1118, 363)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1133, 549)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_paysans():
    zapi_milice_to_hdv()
    pyautogui.scroll(-4)
    time.sleep(t5)
    pyautogui.moveTo(1118, 413)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1211, 666)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_pecheurs():
    zapi_milice_to_hdv()
    pyautogui.scroll(-4)
    time.sleep(t5)
    pyautogui.moveTo(1118, 459)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1214, 337)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_ressources():
    zapi_milice_to_hdv()
    pyautogui.scroll(-4)
    time.sleep(t5)
    pyautogui.moveTo(1118, 507)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1251, 571)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_runes():
    zapi_milice_to_hdv()
    pyautogui.scroll(-4)
    time.sleep(t5)
    pyautogui.moveTo(1118, 553)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1704, 336)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_sculpteurs():
    zapi_milice_to_hdv()
    pyautogui.scroll(-4)
    time.sleep(t5)
    pyautogui.moveTo(1118, 597)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(1401, 374)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')

def go_to_hdv_tailleurs():
    zapi_milice_to_hdv()
    pyautogui.scroll(-4)
    time.sleep(t5)
    pyautogui.moveTo(1118, 644)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.moveTo(756, 608)
    time.sleep(t5)
    pyautogui.click()
    time.sleep(t20)
    pyautogui.press('esc')


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

y_pos = [295, 331, 368, 406, 445, 483, 518, 553, 593, 628, 669, 700]
y_or = [280, 317, 353, 389, 426, 464, 500, 537, 574, 611, 650, 685]

# 1) Update extract to accept start_row (default 0)
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
                    time.sleep(t1)
                    pyautogui.scroll(-4)
                    time.sleep(t1)
                    continue
                idx = extract(idx, start_row=start_row)
            else:
                idx = extract(idx)
        else:
            idx = extract(idx)

        # scroll after each batch
        pyautogui.moveTo(1090, 321)
        time.sleep(t1)
        pyautogui.scroll(-4)
        time.sleep(t1)

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
    go_to_hdv_alchimistes()
