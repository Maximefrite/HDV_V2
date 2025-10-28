import subprocess
import os
import cv2  # For image processing
import numpy as np
import re
import pandas as pd
from datetime import datetime

# Directory containing images
image_folder = '/home/human1/HDV_V2/Screens'

def preprocess_image(image_path):
    """
    Preprocess image: grayscale -> binary threshold -> blur
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return None
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    blurred = cv2.GaussianBlur(thresh, (3, 3), 0)
    return blurred

def ocr_image(image_path, psm=None):
    """
    Run Tesseract OCR on a (preprocessed) image.
    """
    preprocessed = preprocess_image(image_path)
    if preprocessed is None:
        return ""
    temp_image_path = 'temp_image.png'
    cv2.imwrite(temp_image_path, preprocessed)
    try:
        cmd = ['tesseract', temp_image_path, 'stdout']
        if psm is not None:
            cmd.extend(['--psm', str(psm)])
        result = subprocess.run(cmd, capture_output=True, text=True)
        text = result.stdout.strip()
    except Exception as e:
        print(f"OCR failed for {image_path}: {e}")
        text = ""
    finally:
        try:
            os.remove(temp_image_path)
        except Exception:
            pass
    return text

def parse_price(text):
    """
    Extract the first integer-like token from OCR text.
    Accepts digits with optional spaces (e.g., '12 345').
    """
    # remove non-digit/space, keep digits and spaces
    cleaned = re.sub(r'[^\d\s]', '', text)
    cleaned = cleaned.replace(' ', '')
    if cleaned.isdigit():
        try:
            return int(cleaned)
        except ValueError:
            return np.nan
    # fallback: find first contiguous digit run
    m = re.search(r'\d+', cleaned)
    if m:
        try:
            return int(m.group(0))
        except ValueError:
            return np.nan
    return np.nan

def normalize_name(text):
    """
    Choose a reasonable single-line resource name from OCR text.
    Drops separators and empty lines; picks the longest remaining line.
    """
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.startswith('---')]
    if not lines:
        return "Unknown Resource"
    # prefer lines that contain letters
    letter_lines = [ln for ln in lines if re.search(r'[A-Za-z]', ln)]
    candidate_lines = letter_lines if letter_lines else lines
    # choose the longest trimmed line
    name = max(candidate_lines, key=len)
    # collapse multiple spaces
    name = re.sub(r'\s+', ' ', name)
    return name

def current_timestamp():
    """
    Column name like 'YYYYMMDD_HHMMSS'
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def group_files_by_index(folder):
    """
    Finds files matching:
      screenshot_r{i}.png
      screenshot_r{i}_x1.png
      screenshot_r{i}_x10.png
      screenshot_r{i}_x100.png
    Returns dict: { i: {'name': path, 'x1': path, 'x10': path, 'x100': path} }
    """
    pattern = re.compile(r'^screenshot_r(\d+)(?:_(x1|x10|x100))?\.png$', re.IGNORECASE)
    groups = {}
    for fname in os.listdir(folder):
        m = pattern.match(fname)
        if not m:
            continue
        idx = int(m.group(1))
        kind = m.group(2)  # None for the name image
        entry = groups.setdefault(idx, {})
        fpath = os.path.join(folder, fname)
        if kind is None:
            entry['name'] = fpath
        else:
            entry[kind.lower()] = fpath
    return dict(sorted(groups.items(), key=lambda kv: kv[0]))

def create_or_update_dataframe(rows, date_column_name, csv_file='expanded_prices_output.csv'):
    """
    rows: list of tuples (Resource with unit, price)
    Produces/updates a wide CSV with one column per run (date_column_name).
    """
    new_df = pd.DataFrame(rows, columns=['Resource', date_column_name])

    if os.path.isfile(csv_file):
        df_existing = pd.read_csv(csv_file)
        # Drop any unwanted '+ 1h'/' + 2h' columns if present
        unwanted = [col for col in df_existing.columns if '+ 1h' in col or '+ 2h' in col]
        if unwanted:
            df_existing = df_existing.drop(columns=unwanted)
        df_updated = pd.merge(df_existing, new_df, on='Resource', how='outer')
    else:
        df_updated = new_df

    df_updated.sort_values('Resource', inplace=True)
    df_updated.reset_index(drop=True, inplace=True)
    return df_updated

def main():
    # 1) Group files by resource index
    groups = group_files_by_index(image_folder)
    if not groups:
        print("No matching screenshots found.")
        return

    date_col = current_timestamp()
    rows = []  # list of (Resource with unit, price)

    # 2) Iterate in index order
    for idx, files in groups.items():
        name_path = files.get('name')
        x1_path   = files.get('x1')
        x10_path  = files.get('x10')
        x100_path = files.get('x100')

        # Basic presence checks (we'll still try even if some missing)
        if not name_path:
            print(f"[r{idx}] Missing name image (screenshot_r{idx}.png)")
        if not x1_path:
            print(f"[r{idx}] Missing x1 image (screenshot_r{idx}_x1.png)")
        if not x10_path:
            print(f"[r{idx}] Missing x10 image (screenshot_r{idx}_x10.png)")
        if not x100_path:
            print(f"[r{idx}] Missing x100 image (screenshot_r{idx}_x100.png)")

        # 3) OCR name (default PSM) and prices (PSM 7 for single line)
        name_text = ocr_image(name_path, psm=None) if name_path else ""
        resource_name = normalize_name(name_text)

        p1_text = ocr_image(x1_path, psm=7) if x1_path else ""
        p10_text = ocr_image(x10_path, psm=7) if x10_path else ""
        p100_text = ocr_image(x100_path, psm=7) if x100_path else ""

        v1 = parse_price(p1_text)
        v10 = parse_price(p10_text)
        v100 = parse_price(p100_text)

        # 4) Emit 3 rows (Resource expanded)
        rows.append((f"{resource_name} (1 unit)", v1))
        rows.append((f"{resource_name} (10 unit)", v10))
        rows.append((f"{resource_name} (100 unit)", v100))

        # Optional: debug print
        print(f"[r{idx}] {resource_name} -> x1={v1}, x10={v10}, x100={v100}")

    # 5) Create/update DataFrame and CSV
    df = create_or_update_dataframe(rows, date_col)
    print(df)
    df.to_csv('expanded_prices_output.csv', index=False)

if __name__ == '__main__':
    main()

