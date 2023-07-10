import shutil
import os
import gpt_funs
import preprocess
from PIL import Image
from pdf2image import convert_from_path
import pytesseract

PDF_PATH = 'Qpaper.pdf'

path, file_name = os.path.split(PDF_PATH)

preprocess.pdf2folder(PDF_PATH)

gpt_funs.format_entire_pdf("output_folder")
gpt_funs.merge_into_one_text_file("output_folder")

shutil.rmtree('./output_folder')
print("output_folder deleted successfully.")
shutil.rmtree('./Solved_output_folder')
print('Solved_output_folder deleted successfully.')