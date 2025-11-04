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

def take_screenshot(xmin, ymin, xmax, ymax, file_path):
    width = xmax - xmin
    height = ymax - ymin
    img = ImageGrab.grab(bbox=(xmin, ymin, xmin + width, ymin + height))
    img.save(file_path)

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
