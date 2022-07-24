import os
import re
import string
from PyPDF2 import PdfReader
# Handling extraction of text from the pdf files to text files


# Extracts the text from a pdf file
def __extract_text(pdf_route):
    reader = PdfReader(pdf_route)
    text = ""
    print("Extracting: " + pdf_route)
    if reader.isEncrypted:
        print("File encrypted skipping..")
        return ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


# Process the text from the pdf file to remove perform the following operations:
# Lowercase all characters in advance (reducing future computational time during analysis and training)
# Remove punctuation as it is irrelevant to the model
# Remove non-ascii characters as they can make future computation difficult
def __process_text(text):
    text = re.sub(' +', ' ', text.lower().replace("\n", ' ').translate(str.maketrans('', '', string.punctuation)))
    return ''.join(c for c in text if 0 < ord(c) < 127)


# Iterates through all pdf files in the pdf folder to extract the text
def process_pdf_folder():
    directory = 'Data/apt-reports/'
    arr = []
    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            text = __process_text(__extract_text(file))
            if text is not None:
                arr.append((filename, text))
    return arr


# Main function to extract and write pdf text to text files
def __construct_data():
    documents = process_pdf_folder()
    print("Writing files...")
    for document_data in documents:
        if document_data[1] != "":
            with open(f"Data/TextFiles/{document_data[0]}.txt", "w", encoding="utf-8") as f:
                f.write(document_data[1])
    print("Writing complete")


if __name__ == '__main__':
    __construct_data()
