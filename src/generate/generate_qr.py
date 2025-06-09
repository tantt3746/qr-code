import re
import unicodedata
from pathlib import Path

import pandas as pd
import qrcode
import os

# --- Configuration ---
BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)
# The name of your Excel file
EXCEL_FILE = f'{BASE_DIR}/resources/QRCode-TaisanCong.xlsx'
# The main folder where all QR codes will be saved
OUTPUT_DIR = f'{BASE_DIR}/qr_codes_by_department'
# The column name in your Excel file that contains the department
DEPARTMENT_COLUMN = 'Phòng'
INFORMATION_COLUMN = 'Thông tin'
NAME_COLUMN = 'Tên tài sản'

def generate_url_alias(name: str) -> str:
    # Normalize unicode characters (e.g., é → e)
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')

    # Lowercase, remove non-alphanumeric characters, replace spaces with dashes
    name = re.sub(r'[^a-zA-Z0-9\s-]', '', name)  # Remove punctuation
    name = re.sub(r'[\s]+', '-', name)           # Replace whitespace with dash
    return name.lower().strip('-')


def generate_qr_codes():
    """
    Reads data from an Excel file, generates a QR code for each row,
    and saves it in a folder named after the department.
    """
    # 1. Create the main output directory if it doesn't exist
    print(f"Creating main output directory: {OUTPUT_DIR}")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 2. Read the Excel file
    try:
        df = pd.read_excel(EXCEL_FILE)
        print("Excel file loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{EXCEL_FILE}' was not found.")
        print("Please make sure the Excel file is in the same directory as the script.")
        return
    except Exception as e:
        print(f"An error occurred while reading the Excel file: {e}")
        return

    # Check if required columns exist
    required_columns = ['STT', DEPARTMENT_COLUMN, INFORMATION_COLUMN]
    if not all(col in df.columns for col in required_columns):
        print(f"Error: The Excel file must contain the columns: {', '.join(required_columns)}")
        return

    # 3. Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # 4. Extract data from the row
        department = str(row[DEPARTMENT_COLUMN]).strip()
        qr_information = str(row[INFORMATION_COLUMN]).strip()
        name = str(row[NAME_COLUMN]).strip()

        # Sanitize department name to be a valid folder name
        # (e.g., remove special characters, but replacing spaces is fine)
        sane_department_name = department.replace('/', '_').replace('\\', '_')
        department_path = os.path.join(OUTPUT_DIR, sane_department_name)

        # 5. Create a sub-folder for the department if it doesn't exist
        os.makedirs(department_path, exist_ok=True)

        # 6. Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_information)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # 8. Create a unique filename and save the QR code image
        # Sanitize name for the filename
        sane_name = generate_url_alias(name)
        filename = f"{department}_{sane_name}.png"
        file_path = os.path.join(department_path, filename)

        img.save(file_path)

        print(f"-> Generated QR code for '{name}' and saved to '{file_path}'")

    print("\nProcessing complete. All QR codes have been generated.")


if __name__ == "__main__":
    generate_qr_codes()