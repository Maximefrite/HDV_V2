import subprocess
import os
import cv2  # For image processing
import numpy as np
import re
import pandas as pd

# Directory containing images
image_folder = '/home/human1/HDV_V2/Screens'

def preprocess_image(image_path):
    """
    Preprocesses the image by converting it to grayscale, applying thresholding,
    and removing noise to improve OCR accuracy.
    """
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    # Check if image was loaded successfully
    if image is None:
        print(f"Failed to load image: {image_path}")
        return None
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply binary thresholding
    _, thresh_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    # Optionally apply a bit of blurring (this can help with noisy images)
    blurred_image = cv2.GaussianBlur(thresh_image, (3, 3), 0)
    return blurred_image

def ocr_images_in_folder(folder, image_files):
    ocr_results = []
    # Iterate over sorted files with index
    for i, filename in enumerate(image_files, start=1):
        image_path = os.path.join(folder, filename)
        print(f"Processing {image_path} (Image {i})")
        try:
            # Preprocess the image
            preprocessed_image = preprocess_image(image_path)
            if preprocessed_image is not None:
                # Save preprocessed image to a temporary location for OCR
                temp_image_path = 'temp_image.png'
                cv2.imwrite(temp_image_path, preprocessed_image)
                # Determine if we should use --psm 7 based on the image index
                if i % 10 == 1:  # For 1st, 11th, 21st images, etc., no --psm 7
                    result = subprocess.run(
                        ['tesseract', temp_image_path, 'stdout'],
                        capture_output=True,
                        text=True
                    )
                    text = result.stdout
                    print(f"\n===== OCR TEXT for {filename} =====\n{text}\n===============================\n")
                else:  # For all other images, use --psm 7
                    result = subprocess.run(
                        ['tesseract', temp_image_path, 'stdout', '--psm', '7'],
                        capture_output=True,
                        text=True
                    )
                # Append the extracted text to the results list
                ocr_results.append(result.stdout)
                # Remove the temporary image after OCR
                os.remove(temp_image_path)
            else:
                print(f"Skipping {filename} due to preprocessing failure.")
        except Exception as e:
            print(f"Failed to process {image_path}: {e}")
    return ocr_results

def clean_ocr_data(ocr_results):
    cleaned_lines = []
    for text in ocr_results:
        lines = text.split('\n')
        for line in lines:
            # Remove lines starting with "---"
            if line.startswith('---'):
                continue
            elif line.strip():  # Only keep non-empty lines
                cleaned_lines.append(line.strip())
    return cleaned_lines

def load_text_data(cleaned_lines):
    # Extract resources and prices
    resources = []
    prices = []
    current_prices = []
    for line in cleaned_lines:
        # Remove any non-digit characters for price lines
        stripped_line = line.strip()
        if not stripped_line.replace(" ", "").isdigit():  # A line with a resource name
            if current_prices:
                prices.append(current_prices)
                current_prices = []
            resources.append(stripped_line)
        else:
            # Remove spaces in numbers before converting to integer
            line_without_spaces = stripped_line.replace(" ", "")
            try:
                current_prices.append(int(line_without_spaces))
            except ValueError:
                print(f"Skipping invalid price entry: {stripped_line}")
    # Append the last set of prices
    if current_prices:
        prices.append(current_prices)
    return resources, prices

def expand_resource_data(resources, prices):
    # Define resource units
    resource_units = [' (1 unit)', ' (10 unit)', ' (100 unit)']
    # Expand resources with their units
    expanded_resources = []
    for r in resources:
        expanded_resources.extend([r + u for u in resource_units])
    # Flatten prices
    expanded_prices = []
    for price_set in prices:
        expanded_prices.extend(price_set)
    return expanded_resources, expanded_prices

def extract_date_from_filename(filename):
    # Extracts 'YYYYMMDD_HHMMSS' from filenames like 'screenshot_2024-08-11_13-03-31_000.png'
    match = re.search(r'screenshot_(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})', filename)
    if match:
        datetime_str = match.group(1)  # '2024-08-11_13-03-31'
        # Transform to '20240811_130331'
        date_part, time_part = datetime_str.split('_')
        date_part = date_part.replace('-', '')  # '20240811'
        time_part = time_part.replace('-', '')  # '130331'
        return date_part + '_' + time_part
    else:
        return "UnknownDate"

def create_or_update_dataframe(resources, prices, date_column_name, csv_file='expanded_prices_output.csv'):
    # Expand resources and prices
    expanded_resources, expanded_prices = expand_resource_data(resources, prices)
    # Check if lengths of resources and prices are the same
    if len(expanded_resources) != len(expanded_prices):
        print(f"Warning: Mismatch between the number of resources ({len(expanded_resources)}) and prices ({len(expanded_prices)})")
        # Pad the shorter list with NaN values
        if len(expanded_resources) > len(expanded_prices):
            # Add NaN for missing prices
            expanded_prices.extend([np.nan] * (len(expanded_resources) - len(expanded_prices)))
        else:
            # Add NaN for missing resources (this case is less likely)
            expanded_resources.extend(['Unknown Resource'] * (len(expanded_prices) - len(expanded_resources)))
    # Create a DataFrame with the new data
    new_data = pd.DataFrame({
        'Resource': expanded_resources,
        date_column_name: expanded_prices
    })
    # Check if the CSV file exists
    if os.path.isfile(csv_file):
        # Read existing DataFrame
        df_existing = pd.read_csv(csv_file)
        # Remove any unwanted columns like '+ 1h', '+ 2h' if they exist
        unwanted_columns = [col for col in df_existing.columns if '+ 1h' in col or '+ 2h' in col]
        if unwanted_columns:
            df_existing.drop(columns=unwanted_columns, inplace=True)
        # Merge the new data with the existing DataFrame
        df_updated = pd.merge(df_existing, new_data, on='Resource', how='outer')
    else:
        # If the file doesn't exist, create a new DataFrame
        df_updated = new_data
    # Optionally, you can sort the DataFrame by 'Resource'
    df_updated.sort_values('Resource', inplace=True)
    # Reset index
    df_updated.reset_index(drop=True, inplace=True)
    return df_updated

def main():
    # Get the list of image files
    image_files = sorted(f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')))
    if not image_files:
        print("No images found in the folder.")
        return
    # Get the first image filename
    first_image_filename = image_files[0]
    # Extract the date from the filename
    date_column_name = extract_date_from_filename(first_image_filename)
    # Step 1: Run the OCR process
    ocr_results = ocr_images_in_folder(image_folder, image_files)
    # Step 2: Clean the OCR output
    cleaned_lines = clean_ocr_data(ocr_results)
    # Step 3: Process the cleaned data
    resources, prices = load_text_data(cleaned_lines)
    # Step 4: Create or update the DataFrame
    df = create_or_update_dataframe(resources, prices, date_column_name)
    # Display the updated DataFrame
    print(df)
    # Save the DataFrame to CSV
    df.to_csv('expanded_prices_output.csv', index=False)

if __name__ == '__main__':
    main()

