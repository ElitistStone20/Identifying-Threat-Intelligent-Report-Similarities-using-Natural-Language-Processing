import re
import json


# Loads all phrases of interest and constructs the label set from the phrases
# Assigns each phrase with their corresponding label
def construct_labels():
    label_set = []
    with open('labels.json', 'r') as f:
        topics = ["ATTACK_TECHNIQUE", "CYBER_ALIAS", "COMPANY"]
        data = json.load(f)
        for topic in topics:
            for element in data[topic]:
                label_set.append((element, topic))
    return label_set


# Iterates through each entity in the label set and finds all matches
# Iterates through each match and appends a tuple which stores the start and end location of the match in addition to the label
def match_entities(label_set, doc):
    entities = []
    for entity in label_set:
        for match in re.finditer(rf'\b({entity[0]})\b', doc[1]):
            entities.append((match.start(), match.end(), entity[1]))
    return entities


# Constructs the dataset from all matches of entities
def create_dataset(documents):
    print("Performing pattern matching.....")
    entity_list = []
    filenames = []
    label_set = construct_labels()
    for doc in documents:
        entity_list.append((doc[1], {"entities": match_entities(label_set, doc)}))
        filenames.append(doc[0])
    return entity_list, filenames
