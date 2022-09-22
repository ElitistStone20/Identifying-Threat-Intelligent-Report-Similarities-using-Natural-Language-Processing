import os
import ntpath
import spacy.util
from extract_pdf_text import process_pdfs
from Pattern_Matching import create_dataset
from model_development import train_model
from document_simularity import custom_similarity
from Tree import json_to_tree

# Extracts the filename from a given path
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


# partitions the data and filenames list into the training and test set
def partition_data(data, filenames):
    len_data, len_files = len(data), len(filenames)
    if len_data == len_files:
        TRAIN_DATA = data[0:int(round(len_data - len_data / 4))]
        TEST_DATA_RAW = data[(len_data - int(round(len_data / 4))):len_data]
        TEST_DATA = [document[0] for document in TEST_DATA_RAW]
        return TRAIN_DATA, TEST_DATA, filenames[0:int(round(len_data - len_data / 4))], \
               filenames[(len_data - int(round(len_data / 4))):len_data]
    else:
        raise Exception("length of dataset does not match length of filenames")


# Removes documents with no entities from the dataset and filenames list
def filter_docs(docs, filenames):
    i = 0
    while i < len(docs):
        if not len(docs[i].ents) > 0:
            del docs[i]
            del filenames[i]
        i += 1
    return docs, filenames


# Retrieves the user input regarding which label they wish to filter by
def get_user_label():
    label = input("Enter a label to filter by\ncyber_alias, attack_technique or company\nIf neither enter a random character\n").lower()
    if label == "company" or label == "cyber alias" or label == "attack technique":
        return label
    return None


# Main entry point for the software
def main():
    label = get_user_label()
    documents = process_pdfs()
    data, filenames = create_dataset(documents)
    TRAIN_DATA, TEST_DATA, train_filenames, test_filenames = partition_data(data, filenames)
    if not os.path.isdir("./Model"):
        model = train_model(TRAIN_DATA)
    else:
        print("Loading model..........")
        model = spacy.load("./Model")
    test_docs = []
    other_docs = []
    print("Extracting entities from train data.......")
    for doc in TRAIN_DATA:
        other_docs.append(model(doc[0]))
    print("Extracting entities from test documents.......")
    for text in TEST_DATA:
        test_docs.append(model(text))
    print("Filtering documents from test set........")
    test_docs, test_filenames = filter_docs(test_docs, test_filenames)
    print("Filtering documents from train set........")
    other_docs, other_filenames = filter_docs(other_docs, train_filenames)
    print("Calculating percentages.......")
    i = 0
    sims = []
    alias_tree = json_to_tree("cyber_alias", other_docs)
    company_tree = json_to_tree("company", other_docs)
    attack_tree = json_to_tree("attack_technique", other_docs)
    for doc in test_docs:
        sims.append(custom_similarity(other_docs, doc, other_filenames, test_filenames[i], alias_tree, company_tree, attack_tree, label))
        i += 1
    for sim in sims:
        print(f"{path_leaf(sim[0])} most similar to: {path_leaf(sim[1])}. Score {sim[2]}%\n")


if __name__ == '__main__':
    main()
