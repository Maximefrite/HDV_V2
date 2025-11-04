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
from sub_category import (
    sub_category_2, sub_category_3, sub_category_4, sub_category_5,
    sub_category_6, sub_category_7, sub_category_8, sub_category_9,
    sub_category_10, sub_category_11, sub_category_12, sub_category_13,
    sub_category_14, sub_category_15, sub_category_16, sub_category_17,
    sub_category_18, sub_category_19, sub_category_20, sub_category_21,
    sub_category_22, sub_category_23
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

def extract_all_hdv():
    # HDV ALCHIMISTES
    go_to_hdv_alchimistes()
    file_path = '/home/human1/HDV_V2/Screens/Alchimistes/Materiel_dalchimie'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Alchimistes/Materia'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Alchimistes/Objet_de_dons'
    run_once_or_full()
    sub_category_4()
    file_path = '/home/human1/HDV_V2/Screens/Alchimistes/Potion'
    run_once_or_full()
    sub_category_9()
    file_path = '/home/human1/HDV_V2/Screens/Alchimistes/Potion_de_forgemagie'
    run_once_or_full()
    sub_category_10()
    file_path = '/home/human1/HDV_V2/Screens/Alchimistes/Teinture'
    run_once_or_full()

    # HDV BIJOUTIERS
    go_to_hdv_bijoutiers()
    file_path = '/home/human1/HDV_V2/Screens/Bijoutier/Amulette'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Bijoutier/Anneau'
    run_once_or_full()

    # HDV BOULANGERS
    go_to_hdv_boulangers()
    file_path = '/home/human1/HDV_V2/Screens/Boulanger/Friandise'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Boulanger/Pain'
    run_once_or_full()

    # HDV PAYSANS
    go_to_hdv_paysans()
    file_path = '/home/human1/HDV_V2/Screens/Paysan/Cereale'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Paysan/Farine'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Paysan/Huile'
    run_once_or_full()

    # HDV SCULPTEURS
    go_to_hdv_sculpteurs()
    file_path = '/home/human1/HDV_V2/Screens/Sculpteur/Arc'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Sculpteur/Baton'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Sculpteur/Baguette'
    run_once_or_full()

    # HDV MINEURS
    go_to_hdv_mineurs()
    file_path = '/home/human1/HDV_V2/Screens/Mineur/Alliage'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Mineur/Minerai'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Mineur/Pierre_brute'
    run_once_or_full()
    sub_category_4()
    file_path = '/home/human1/HDV_V2/Screens/Mineur/Pierre_magique'
    run_once_or_full()
    sub_category_5()
    file_path = '/home/human1/HDV_V2/Screens/Mineur/Pierre_precieuse'
    run_once_or_full()

    # HDV PECHEURS
    go_to_hdv_pecheurs()
    file_path = '/home/human1/HDV_V2/Screens/Pecheur/Poisson'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Pecheur/Poisson_comestible'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Pecheur/Poisson_vide'
    run_once_or_full()

    # HDV RESSOURCES
    go_to_hdv_ressources()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Aile'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Carapace'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Coquille'
    run_once_or_full()
    sub_category_4()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Cuir'
    run_once_or_full()
    sub_category_5()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Etoffe'
    run_once_or_full()
    sub_category_6()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Fleur'
    run_once_or_full()
    sub_category_7()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Fruit'
    run_once_or_full()
    sub_category_8()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Gelee'
    run_once_or_full()
    sub_category_9()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Graine'
    run_once_or_full()
    sub_category_10()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Laine'
    run_once_or_full()
    sub_category_11()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Legume'
    run_once_or_full()
    sub_category_12()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Oeil'
    run_once_or_full()
    sub_category_13()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Oeuf'
    run_once_or_full()
    sub_category_14()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Oreille'
    run_once_or_full()
    sub_category_15()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Os'
    run_once_or_full()
    sub_category_16()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Patte'
    run_once_or_full()
    sub_category_17()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Peau'
    run_once_or_full()
    sub_category_18()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Plante'
    run_once_or_full()
    sub_category_19()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Plume'
    run_once_or_full()
    sub_category_20()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Poil'
    run_once_or_full()
    sub_category_21()
    file_path = '/home/human1/HDV_V2/Screens/Ressource/Poudre'
    run_once_or_full()
    sub_category_22()
    file_path ='/home/human1/HDV_V2/Screens/Ressource/Queue'
    run_once_or_full()
    sub_category_23()
    file_path ='/home/human1/HDV_V2/Screens/Ressource/Ressource'
    run_once_or_full()

    # HDV RUNES
    go_to_hdv_runes()
    file_path = '/home/human1/HDV_V2/Screens/Rune/Rune'
    run_once_or_full()

    # HDV BRICOLEURS
    go_to_hdv_bricoleurs()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Bricoleur/Clefs'
    run_once_or_full()

    # HDV FORGERONS
    go_to_hdv_forgerons()
    file_path = '/home/human1/HDV_V2/Screens/Forgeron/Dague'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Forgeron/Epee'
    run_once_or_full()
    sub_category_4()
    file_path = '/home/human1/HDV_V2/Screens/Forgeron/Hache'
    run_once_or_full()
    sub_category_5()
    file_path = '/home/human1/HDV_V2/Screens/Forgeron/Marteau'
    run_once_or_full()
    sub_category_6()
    file_path = '/home/human1/HDV_V2/Screens/Forgeron/Pelle'
    run_once_or_full()

    # HDV BIJOUTIERS
    go_to_hdv_bijoutiers()
    file_path = '/home/human1/HDV_V2/Screens/Bijoutier/Amulette'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Bijoutier/Anneau'
    run_once_or_full()

    # HDV CORDONNIERS
    go_to_hdv_cordonniers()
    file_path = '/home/human1/HDV_V2/Screens/Cordonnier/Botte'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Cordonnier/Ceinture'
    run_once_or_full()

    # HDV BUCHERONS
    go_to_hdv_bucherons()
    file_path = '/home/human1/HDV_V2/Screens/Bucheron/Bois'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Bucheron/Bourgeon'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Bucheron/Ecorce'
    run_once_or_full()
    sub_category_4()
    file_path = '/home/human1/HDV_V2/Screens/Bucheron/Planche'
    run_once_or_full()
    sub_category_5()
    file_path = '/home/human1/HDV_V2/Screens/Bucheron/Racine'
    run_once_or_full()

    # HDV TAILLEURS
    go_to_hdv_tailleurs()
    file_path = '/home/human1/HDV_V2/Screens/Tailleur/Cape'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Tailleur/Chapeau'
    run_once_or_full()
    sub_category_5()
    file_path = '/home/human1/HDV_V2/Screens/Tailleur/Sac_a_dos'
    run_once_or_full()

    # HDV DOCUMENTS
    go_to_hdv_documents()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Document/Parchemin_dexperience'
    run_once_or_full()
    sub_category_4()
    file_path = '/home/human1/HDV_V2/Screens/Document/Parchemin_de_caracteristique'
    run_once_or_full()

    # HDV BOUCHERS
    go_to_hdv_bouchers()
    file_path = '/home/human1/HDV_V2/Screens/Boucher/Viande'
    run_once_or_full()
    sub_category_2()
    file_path = '/home/human1/HDV_V2/Screens/Boucher/Viande_comestible'
    run_once_or_full()
    sub_category_3()
    file_path = '/home/human1/HDV_V2/Screens/Boucher/Viande_conservee' 
    run_once_or_full()


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
    extract_all_hdv()
