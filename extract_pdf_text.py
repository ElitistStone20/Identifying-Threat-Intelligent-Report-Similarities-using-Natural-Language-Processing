import os
import re
from PyPDF2 import PdfReader


# Extracts text from the pdf file using the file's route.
# If the file is encrypted the file is skipped
def __extract_text(route):
    reader = PdfReader(route)
    text = ""
    print("Extracting: " + route)
    if reader.isEncrypted:
        print("File encrypted skipping......")
        return ""
    for i in range(reader.numPages):
        page = reader.getPage(i)
        text += page.extract_text()
    return text


# Removes mass white-spacing, lower-cases text and removes newlines.
# Additionally non-ascii characters are removed to reduce complexity with handling characters from different langauges.
def __process_text(text):
    text = re.sub(' +', ' ', text.lower().replace('\n', ''))
    return ''.join(c for c in text if 0 < ord(c) < 127)


# Iterates over each file in directory and extracts the text from the file.
# Appends the filename and text to array
def __process_folder(route):
    arr = []
    for filename in os.listdir(route):
        file = os.path.join(route, filename)
        if os.path.isfile(file):
            text = __process_text(__extract_text(file))
            if text is not None:
                arr.append((filename, text))
    return arr


# Prompts for directory input and if the directory is valid returns the data extracted from the pdf files
def process_pdfs():
    route = input("Enter directory of PDF files:\n")
    if os.path.isdir(route):
        return __process_folder(route)
