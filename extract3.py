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

# Timings
t1 = 0.1
t2 = 0.2
t5 = 0.5
t10 = 1.0
t20 = 2.0


# -------------------------
# Color Detection Utilities
# -------------------------

def is_need_to_scrol():
    return pyautogui.pixel(1092, 302) == (81, 74, 60)

def is_end_of_scrol():
    return pyautogui.pixel(1089, 692) == (81, 74, 60)

def is_pixel_color_orange(y):
    return pyautogui.pixel(658, y) == (255, 153, 17)


# -------------------------
# Screenshot Functions
# -------------------------

def screen_nom_ressource(i, base_path):
    xmin, ymin, xmax, ymax = 1151, 146, 1753, 184
    file_path = os.path.join(base_path, f'screenshot_r{i}.png')
    take_screenshot(xmin, ymin, xmax, ymax, file_path)

def screen_prix_x1(i, base_path):
    xmin, ymin, xmax, ymax = 1190, 560, 1346, 594
    file_path = os.path.join(base_path, f'screenshot_r{i}_x1.png')
    take_screenshot(xmin, ymin, xmax, ymax, file_path)

def screen_prix_x10(i, base_path):
    xmin, ymin, xmax, ymax = 1351, 560, 1507, 594
    file_path = os.path.join(base_path, f'screenshot_r{i}_x10.png')
    take_screenshot(xmin, ymin, xmax, ymax, file_path)

def screen_prix_x100(i, base_path):
    xmin, ymin, xmax, ymax = 1512, 560, 1668, 594
    file_path = os.path.join(base_path, f'screenshot_r{i}_x100.png')
    take_screenshot(xmin, ymin, xmax, ymax, file_path)


# -------------------------
# Screen Coordinates
# -------------------------

y_pos = [295, 331, 368, 406, 445, 483, 518, 553, 593, 628, 669, 700]
y_or  = [280, 317, 353, 389, 426, 464, 500, 537, 574, 611, 650, 685]


# -------------------------
# Extraction Logic
# -------------------------

def extract(start_i=1, start_row=0, base_path='/home/human1/HDV_V2/Screens'):
    i = start_i
    rows = y_pos[start_row:]
    for y in rows:
        time.sleep(t1)
        pyautogui.moveTo(1000, y)
        time.sleep(t1)
        pyautogui.click()
        time.sleep(t2)
        screen_nom_ressource(i, base_path)
        screen_prix_x1(i, base_path)
        screen_prix_x10(i, base_path)
        screen_prix_x100(i, base_path)
        i += 1
    return i


def extract_until_scrol_down(base_path):
    idx = 1
    first_page = True

    while True:
        if first_page:
            idx = extract(idx, base_path=base_path)
            first_page = False
        else:
            found_index = None
            for j, y in enumerate(y_or):
                if is_pixel_color_orange(y):
                    found_index = j
                    break

            if found_index is not None:
                start_row = found_index + 1
                if start_row < len(y_pos):
                    idx = extract(idx, start_row=start_row, base_path=base_path)
            else:
                idx = extract(idx, base_path=base_path)

        if is_end_of_scrol():
            break

        pyautogui.moveTo(1090, 321)
        time.sleep(t1)
        pyautogui.scroll(-4)
        time.sleep(t1)


def run_once_or_full(base_path):
    if not is_need_to_scrol():
        extract(start_i=1, start_row=0, base_path=base_path)
    else:
        extract_until_scrol_down(base_path)


# -------------------------
# HDV Extraction Sequence
# -------------------------

def extract_all_hdv():
    # HDV ALCHIMISTES
    go_to_hdv_alchimistes()
    run_once_or_full('/home/human1/HDV_V2/Screens/Alchimistes/Materiel_dalchimie')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Alchimistes/Materia')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Alchimistes/Objet_de_dons')
    sub_category_4()
    run_once_or_full('/home/human1/HDV_V2/Screens/Alchimistes/Potion')
    sub_category_9()
    run_once_or_full('/home/human1/HDV_V2/Screens/Alchimistes/Potion_de_forgemagie')
    sub_category_10()
    run_once_or_full('/home/human1/HDV_V2/Screens/Alchimistes/Teinture')

    # HDV BIJOUTIERS
    go_to_hdv_bijoutiers()
    run_once_or_full('/home/human1/HDV_V2/Screens/Bijoutier/Amulette')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Bijoutier/Anneau')

    # HDV BOULANGERS
    go_to_hdv_boulangers()
    run_once_or_full('/home/human1/HDV_V2/Screens/Boulanger/Friandise')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Boulanger/Pain')

    # HDV PAYSANS
    go_to_hdv_paysans()
    run_once_or_full('/home/human1/HDV_V2/Screens/Paysan/Cereale')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Paysan/Farine')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Paysan/Huile')

    # HDV SCULPTEURS
    go_to_hdv_sculpteurs()
    run_once_or_full('/home/human1/HDV_V2/Screens/Sculpteur/Arc')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Sculpteur/Baton')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Sculpteur/Baguette')

    # HDV MINEURS
    go_to_hdv_mineurs()
    run_once_or_full('/home/human1/HDV_V2/Screens/Mineur/Alliage')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Mineur/Minerai')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Mineur/Pierre_brute')
    sub_category_4()
    run_once_or_full('/home/human1/HDV_V2/Screens/Mineur/Pierre_magique')
    sub_category_5()
    run_once_or_full('/home/human1/HDV_V2/Screens/Mineur/Pierre_precieuse')

    # HDV PECHEURS
    go_to_hdv_pecheurs()
    run_once_or_full('/home/human1/HDV_V2/Screens/Pecheur/Poisson')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Pecheur/Poisson_comestible')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Pecheur/Poisson_vide')

    # HDV RESSOURCES
    go_to_hdv_ressources()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Aile')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Carapace')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Coquille')
    sub_category_4()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Cuir')
    sub_category_5()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Etoffe')
    sub_category_6()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Fleur')
    sub_category_7()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Fruit')
    sub_category_8()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Gelee')
    sub_category_9()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Graine')
    sub_category_10()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Laine')
    sub_category_11()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Legume')
    sub_category_12()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Oeil')
    sub_category_13()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Oeuf')
    sub_category_14()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Oreille')
    sub_category_15()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Os')
    sub_category_16()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Patte')
    sub_category_17()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Peau')
    sub_category_18()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Plante')
    sub_category_19()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Plume')
    sub_category_20()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Poil')
    sub_category_21()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Poudre')
    sub_category_22()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Queue')
    sub_category_23()
    run_once_or_full('/home/human1/HDV_V2/Screens/Ressource/Ressource')

    # HDV RUNES
    go_to_hdv_runes()
    run_once_or_full('/home/human1/HDV_V2/Screens/Rune/Rune')

    # HDV BRICOLEURS
    go_to_hdv_bricoleurs()
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Bricoleur/Clefs')

    # HDV FORGERONS
    go_to_hdv_forgerons()
    run_once_or_full('/home/human1/HDV_V2/Screens/Forgeron/Dague')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Forgeron/Epee')
    sub_category_4()
    run_once_or_full('/home/human1/HDV_V2/Screens/Forgeron/Hache')
    sub_category_5()
    run_once_or_full('/home/human1/HDV_V2/Screens/Forgeron/Marteau')
    sub_category_6()
    run_once_or_full('/home/human1/HDV_V2/Screens/Forgeron/Pelle')

    # HDV CORDONNIERS
    go_to_hdv_cordonniers()
    run_once_or_full('/home/human1/HDV_V2/Screens/Cordonnier/Botte')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Cordonnier/Ceinture')

    # HDV BUCHERONS
    go_to_hdv_bucherons()
    run_once_or_full('/home/human1/HDV_V2/Screens/Bucheron/Bois')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Bucheron/Bourgeon')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Bucheron/Ecorce')
    sub_category_4()
    run_once_or_full('/home/human1/HDV_V2/Screens/Bucheron/Planche')
    sub_category_5()
    run_once_or_full('/home/human1/HDV_V2/Screens/Bucheron/Racine')

    # HDV TAILLEURS
    go_to_hdv_tailleurs()
    run_once_or_full('/home/human1/HDV_V2/Screens/Tailleur/Cape')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Tailleur/Chapeau')
    sub_category_5()
    run_once_or_full('/home/human1/HDV_V2/Screens/Tailleur/Sac_a_dos')

    # HDV DOCUMENTS
    go_to_hdv_documents()
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Document/Parchemin_dexperience')
    sub_category_4()
    run_once_or_full('/home/human1/HDV_V2/Screens/Document/Parchemin_de_caracteristique')

    # HDV BOUCHERS
    go_to_hdv_bouchers()
    run_once_or_full('/home/human1/HDV_V2/Screens/Boucher/Viande')
    sub_category_2()
    run_once_or_full('/home/human1/HDV_V2/Screens/Boucher/Viande_comestible')
    sub_category_3()
    run_once_or_full('/home/human1/HDV_V2/Screens/Boucher/Viande_conservee')


# -------------------------
# Main
# -------------------------

if __name__ == "__main__":
    screenshots_dir = '/home/human1/HDV_V2/Screens'
    for filename in os.listdir(screenshots_dir):
        file_path = os.path.join(screenshots_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error: {e}")

    extract_all_hdv()
