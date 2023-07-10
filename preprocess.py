import os
import gpt_funs
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# recieve pdf file path and splits it into pages and converts eah page to a text file and saves it to a folder
def pdf2folder(pdf_path):
    doc = convert_from_path(pdf_path, poppler_path=r"C:/poppler-23.05.0/Library/bin")
    path, file_name = os.path.split(pdf_path)
    file_base_name, file_extension = os.path.splitext(file_name)
    output_folder = f"./uploads/text/{file_base_name}"  # Specify the output folder name
    os.makedirs(output_folder, exist_ok=True)  # Create the output folder if it doesn't exist

    for page_number, page_data in enumerate(doc):
        output_file = f"{output_folder}/{file_name}_page{page_number + 1}.txt"  # Generate the output file name

        with open(output_file, 'w', encoding='utf-8') as f:
            txt = pytesseract.image_to_string(page_data, lang='eng')
            f.write(txt)

    print("Text extracted and saved to separate files in", output_folder)

# # recieve pdf file path and splits it into pages and converts eah page to an image file and saves it to a folder
def pdf2img(path):
    doc = convert_from_path(path, poppler_path=r"C:/poppler-23.05.0/Library/bin", dpi=300)
    path, file_name = os.path.split(path)
    file_base_name, file_extension = os.path.splitext(file_name)
    output_folder = f"./uploads/"  # Specify the output folder name
    os.makedirs(f"{output_folder}{file_base_name}", exist_ok=True)  # Create the output folder if it doesn't exist

    for page_number, page_data in enumerate(doc):
        output_file = f"{output_folder}{file_base_name}/{file_name}_page{page_number + 1}.jpg"  # Generate the output file name
        page_data.save(output_file, 'JPEG')

    print("Image extracted and saved to separate files in", output_folder)

    # return page_number
