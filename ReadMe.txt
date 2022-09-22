Protptype implementation of the document similarity solution:

Requirments:
    - Python 3
    - Imports:
        - spacy
        - ntpath
        - re
        - PyPDF2
        - thinc

Execution Instructions:
- Run main.py.
- You will be prompted to enter a label (if any) you wish to filter by.
    - If you do not want to filter by any labels, enter a random string of 1 or more characters
- Next you will be propted to enter the directory where the APT reports downloaded are situated.
- With all the information provided the text from the PDFs will be extracted, prepossed and annoted.
- If the Model folder is present then the model will be loaded and the entities will be extracted from the training data and test data.
    - If thhe Model folder is not present a new model will be trained on the train data, you will then need to re-run the main file.
- The entities extracted will be ussed to determine the similarity between the documents.
- Finally, the similar documents and their percentage similarity will be printed to the console.